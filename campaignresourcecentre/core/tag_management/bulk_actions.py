import json
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page, Revision
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.wagtailreacttaxonomy.models import TaxonomyTerms
from .utils import get_page_taxonomy_tags
from .forms import ManageTagsForm
from wagtail import hooks
from logging import getLogger

logger = getLogger(__name__)


@hooks.register("register_log_actions")
def remove_tags_action(actions):
    actions.register_action(
        "remove_tags", "Bulk action: Remove tags", "Bulk action: Remove tags"
    )


@hooks.register("register_log_actions")
def add_tags_action(actions):
    actions.register_action(
        "add_tags",
        "Bulk action: Add tags",
        "Bulk action: Add tags",
    )


class TagBulkAction(PageBulkAction):
    models = [Page]
    form_class = ManageTagsForm


class BaseTagBulkAction(PageBulkAction):
    models = [Page]
    form_class = ManageTagsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_type"] = self.action_type
        return context

    def post(self, request, *args, **kwargs):
        """Handle custom post actions for going back and previewing changes."""
        if request.POST.get("next_action") == "go_back":
            ctx = self.get_context_data(**kwargs)
            ctx["form"] = self.form_class(request.POST or None)
            return self.render_to_response(ctx)

        if request.POST.get("next_action") == "preview_changes":
            ctx = self.get_context_data(**kwargs)
            ctx["preview_changes"] = True
            ctx["form"] = self.form_class(request.POST)
            self.is_preview = True
            return self._on_preview(request, ctx)

        if request.POST.get("next_action") == "apply_changes":
            ctx = self.get_context_data(**kwargs)
            return self._on_apply(request, ctx)

        return super().post(request, *args, **kwargs)

    def check_perm(self, page):
        if page.alias_of_id:
            return False
        return isinstance(page.specific, (CampaignPage, ResourcePage))

    def _on_preview(self, request, ctx):
        """What happens when user previews changes."""
        raise NotImplementedError

    def _get_draft_tags(self, page):
        """Get tags from the draft version of the page."""
        if not page.latest_revision:
            return None

        if (
            page.live
            and page.live_revision
            and page.latest_revision.id == page.live_revision.id
        ):
            return None

        source = page.latest_revision.as_object()
        return get_page_taxonomy_tags(source)

    def _get_live_tags(self, page):
        """Get tags to use as the base for operations."""
        if page.live:
            source = (
                page.live_revision.as_object() if page.live_revision else page.specific
            )
        else:
            source = (
                page.latest_revision.as_object()
                if page.latest_revision
                else page.specific
            )

        return get_page_taxonomy_tags(source)

    def has_drafts(self, page):
        """Check if the page has both live and draft versions."""
        if not page.live:
            return False

        if (
            page.live_revision
            and page.latest_revision
            and page.live_revision.id != page.latest_revision.id
        ):
            return True

        return False

    def _update_page_revision(
        self, source, tags, user, publish=False, keep_draft_latest=False
    ):
        """Update page revision with new tags."""

        page_object = source.as_object() if isinstance(source, Revision) else source

        current_tags = get_page_taxonomy_tags(page_object)
        has_changes = current_tags != tags
        page_object.taxonomy_json = json.dumps(tags)

        if tags or keep_draft_latest:
            # For drafts we want to always mark as changed so has_unpublished_changes is set
            mark_as_changed = has_changes if publish else True
            revision = page_object.save_revision(
                user=user,
                changed=mark_as_changed,
                log_action=self.action_type if has_changes else False,
            )
            if publish:
                revision.publish(user=user, log_action=True)
        return has_changes

    def _save_tags(self, page, live_tags, draft_tags, user):
        if page.alias_of_id:
            raise ValueError("Cannot modify tags on alias pages")

        # Draft only pages
        if not page.live:
            return self._update_page_revision(
                page.latest_revision or page,
                draft_tags,
                user=user,
                publish=False,
            )

        # Published page - check if draft exists as well
        draft_revision = (
            page.latest_revision
            if self.has_drafts(page)
            else None
        )
        
        update_published = False
        if page.live_revision:
            # Published page - build from snapshot, update tags and then publish that revision
            update_published = self._update_page_revision(
                page.live_revision,
                live_tags,
                user=user,
                publish=True,
                keep_draft_latest=False,
            )

        # If there was a draft, keep that as the latest revision and update its tags
        update_draft = False
        if draft_revision:
            update_draft = self._update_page_revision(
                draft_revision,
                draft_tags or live_tags,
                user=user,
                publish=False,
                keep_draft_latest=True,
            )

        return update_published or update_draft


class RemoveTagsBulkAction(BaseTagBulkAction):
    template_name = "tag_management/remove-tags-form.html"
    result_template = "tag_management/results.html"
    display_name = "Remove Tags"
    aria_label = "Remove tags from selected pages"
    action_type = "remove_tags"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context.get("items", [])
        for page in items:
            item = page["item"]
            page_tags = self._get_live_tags(item)
            page.update(
                {
                    "tags": page_tags,
                }
            )

        context["items"] = items
        return context

    def _on_apply(self, request, ctx):
        base_tags_for_removal = json.loads(request.POST.get("tags_to_remove", "{}"))
        items = ctx.get("items", [])
        logger.info(
            "Starting tag removal bulk action",
            extra={
                "page_ids": [item["item"].id for item in items],
                "tags_to_remove": base_tags_for_removal,
            },
        )

        failed = 0
        modified = 0
        errors = {}

        for item in items:
            page = item["item"]
            tags_to_remove = base_tags_for_removal.get(str(page.id), [])

            try:
                live_tags = self._calculate_final_tags(
                    self._get_live_tags(page), tags_to_remove
                )
                draft_tags = None
                if self.has_drafts(page):
                    draft_current = self._get_draft_tags(page)
                    draft_tags = self._calculate_final_tags(
                        draft_current, tags_to_remove
                    )
                    
                logger.error(f"Removing tags from page ID {page.id}: {tags_to_remove}")
                logger.info(f"draft_tags {draft_tags}",)
                logger.info(f"live_tags {live_tags}",)

                self._save_tags(page, live_tags, draft_tags, request.user)
                modified += 1
            except Exception as e:
                errors[page.id] = str(e)
                failed += 1
                logger.error(f"Error removing tags from page ID {page.id}: {e}")

        page_ids = [item["item"].id for item in items]
        fresh_pages = Page.objects.filter(id__in=page_ids).specific()
        fresh_items = []
        for page in fresh_pages:
            fresh_items.append(
                {
                    "item": page,
                    "tags": self._get_live_tags(page),
                    "status": "error" if page.id in errors else "updated",
                    "error": errors.get(page.id),
                }
            )

        ctx.update(
            {
                "items": fresh_items,
                "num_modified": modified,
                "num_failed": failed,
                "next_url": self.next_url,
            }
        )
        return render(request, self.result_template, ctx)

    def _on_preview(self, request, ctx):
        items = ctx.get("items", [])
        tags_to_remove = json.loads(request.POST.get("tags_to_remove", "[]"))
        ctx["items"] = self._calculate_changes(items, tags_to_remove)

        return render(request, self.template_name, ctx)

    def _calculate_changes(self, pages, tags={}):
        return_items = []
        for page in pages:
            item = page["item"]

            tags_to_remove = tags.get(str(item.id), [])
            current_tags = self._get_live_tags(item)
            new_tags = []

            for tag in current_tags:

                tag["status"] = (
                    "removed" if tag["code"] in tags_to_remove else "unchanged"
                )

                new_tags.append(tag)

            removed_count = len([t for t in new_tags if t["status"] == "removed"])

            return_items.append(
                {
                    "item_id": item.id,
                    "item_name": item.get_admin_display_title(),
                    "item": item,
                    "tags": new_tags,
                    "removed_count": removed_count,
                    "has_changes": removed_count > 0,
                }
            )

        return return_items

    def _calculate_final_tags(self, current_tags, tags_to_remove):
        return [t for t in current_tags if t["code"] not in tags_to_remove]


class AddTagsBulkAction(BaseTagBulkAction):
    display_name = "Add Tags"
    aria_label = "Add tags to selected pages"
    action_type = "add_tags"
    template_name = "tag_management/add-tags-form.html"
    result_template = "tag_management/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "is_preview"):
            context["taxonomy_terms_json"] = self._get_taxonomy_terms()
        return context

    def _get_taxonomy_terms(self):
        try:
            taxonomy_data = TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy")
            return taxonomy_data.terms_json
        except TaxonomyTerms.DoesNotExist:
            logger.error("Taxonomy terms not found")
            return []

    def _on_apply(self, request, ctx):
        tags_to_add = json.loads(request.POST.get("tags_to_add", "[]"))
        operation_mode = request.POST.get("tag_operation_mode", "merge")
        items = ctx.get("items", [])

        failed = 0
        modified = 0
        errors = {}

        for item in items:
            page = item["item"]

            try:
                live_tags = self._calculate_final_tags(
                    self._get_live_tags(page), tags_to_add, operation_mode
                )

                draft_tags = None
                if page.has_unpublished_changes:
                    draft_current = self._get_draft_tags(page)
                    draft_tags = self._calculate_final_tags(
                        draft_current, tags_to_add, operation_mode
                    )

                self._save_tags(page, live_tags, draft_tags, request.user)
                modified += 1
            except Exception as e:
                errors[page.id] = str(e)
                failed += 1
                logger.error(f"Error adding tags to page ID {page.id}: {e}")

        page_ids = [item["item"].id for item in items]
        fresh_pages = Page.objects.filter(id__in=page_ids).specific()
        fresh_items = []
        for page in fresh_pages:
            fresh_items.append(
                {
                    "item": page,
                    "tags": self._get_live_tags(page),
                    "status": "error" if page.id in errors else "updated",
                    "error": errors.get(page.id),
                }
            )

        ctx.update(
            {
                "items": fresh_items,
                "num_modified": modified,
                "num_failed": failed,
                "operation_mode": operation_mode,
                "next_url": self.next_url,
            }
        )
        return render(request, self.result_template, ctx)

    def _on_preview(self, request, ctx):
        items = ctx.get("items", [])
        tags_to_add = json.loads(request.POST.get("tags_to_add", "[]"))
        operation_mode = request.POST.get("tag_operation_mode", "merge")
        ctx["items"] = self._calculate_changes(items, tags_to_add, operation_mode)
        return render(request, self.template_name, ctx)

    def _calculate_changes(self, pages, tags_to_add=[], operation_mode="merge"):
        return_items = []
        for page in pages:
            item = page["item"]
            result = self._get_tags_with_status(item, tags_to_add, operation_mode)

            return_items.append(
                {
                    "item_id": item.id,
                    "item_name": item.get_admin_display_title(),
                    "item": item,
                    "tags": result["tags"],
                    "draft_page_tags": page.get("draft_page_tags", []),
                    "added_count": result["added_count"],
                    "removed_count": result["removed_count"],
                    "has_changes": result["has_changes"],
                }
            )

        return return_items

    def _calculate_final_tags(self, current_tags, tags_to_add, operation_mode):
        if operation_mode == "replace":
            return tags_to_add
        else:  # merge
            existing_codes = {t["code"] for t in current_tags}
            return current_tags + [
                t for t in tags_to_add if t["code"] not in existing_codes
            ]

    def _get_tags_with_status(self, page, tags, operation_mode="merge"):
        current_tags = self._get_live_tags(page)
        if tags is None:
            return {
                "tags": [{**tag, "status": "unchanged"} for tag in current_tags],
                "added_count": 0,
                "removed_count": 0,
                "has_changes": False,
            }

        if operation_mode == "replace":
            new_tags = tags
        else:
            existing_codes = {t["code"] for t in current_tags}
            new_tags = current_tags + [
                t for t in tags if t["code"] not in existing_codes
            ]

        current_codes = {t["code"] for t in current_tags}
        new_codes = {t["code"] for t in new_tags}
        tags_with_status = []

        for tag in new_tags:
            tags_with_status.append(
                {
                    **tag,
                    "status": (
                        "added" if tag["code"] not in current_codes else "unchanged"
                    ),
                }
            )

        for tag in current_tags:
            if tag["code"] not in new_codes:
                tags_with_status.append({**tag, "status": "removed"})

        added_count = len([t for t in tags_with_status if t["status"] == "added"])
        removed_count = len([t for t in tags_with_status if t["status"] == "removed"])

        return {
            "tags": tags_with_status,
            "added_count": added_count,
            "removed_count": removed_count,
            "has_changes": added_count > 0 or removed_count > 0,
        }
