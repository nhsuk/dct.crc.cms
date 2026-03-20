import json
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page, Revision
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction
from django.core.exceptions import ValidationError

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.wagtailreacttaxonomy.models import (
    TaxonomyTerms,
    load_campaign_topics,
    get_crc_taxonomy,
)
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


@hooks.register("register_log_actions")
def set_topic_tags_from_csv_action(actions):
    actions.register_action(
        "set_topic_tags_from_csv",
        "API: Set topic tags from CSV",
        "API: Set topic tags from CSV",
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

    def _get_current_tags(self, page):
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

    def _has_unpublished_changes(self, page):
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

    def _update_page_revision(self, source, tags, user, publish=False):
        """Update page revision with new tags."""

        page_object = source.as_object() if isinstance(source, Revision) else source

        current_tags = get_page_taxonomy_tags(page_object)
        has_changes = current_tags != tags
        page_object.taxonomy_json = json.dumps(tags)

        # For draft onlys we want to always mark as changed so has_unpublished_changes is set
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
                draft_tags or live_tags,
                user=user,
                publish=False,
            )

        # Published page - check if draft exists as well
        draft_revision = (
            page.latest_revision if self._has_unpublished_changes(page) else None
        )

        update_published = False
        if page.live_revision:
            # Published page - build from snapshot, update tags and then publish that revision
            update_published = self._update_page_revision(
                page.live_revision,
                live_tags,
                user=user,
                publish=True,
            )

        # If there was a draft, keep that as the latest revision and update its tags
        update_draft = False
        if draft_revision:
            update_draft = self._update_page_revision(
                draft_revision,
                draft_tags or live_tags,
                user=user,
                publish=False,
            )

        return update_published or update_draft

    def _get_topic_codes(self, data=None):
        if data is None:
            data = get_crc_taxonomy()

        # Load campaign topics from the Topic model
        load_campaign_topics(data)

        topic_vocab = next((v for v in data if v.get("code") == "TOPIC"), None)
        if not topic_vocab:
            raise ValidationError("No topic vocabulary found in taxonomy")

        topic_codes = {
            child.get("code")
            for child in topic_vocab.get("children", [])
            if child.get("code")
        }
        if not topic_codes:
            raise ValidationError("No topic vocabulary found in taxonomy")

        return topic_codes

    def _ensure_has_topic_tag(self, tags, topic_codes, action_type="add"):
        """Validate that at least one TOPIC tag exists."""
        if not any(tag.get("code") in topic_codes for tag in tags):
            if action_type == "remove":
                raise ValidationError("Please leave at least one topic tag")
            else:
                raise ValidationError("Please select at least one topic tag")


class RemoveTagsBulkAction(BaseTagBulkAction):
    template_name = "tag_management/remove-tags-form.html"
    result_template = "tag_management/results.html"
    display_name = "Remove Tags"
    aria_label = "Remove tags from selected pages"
    action_type = "remove_tags"

    def form_valid(self, form):
        super(ManageTagsBulkAction, self).form_valid(form)

        return render(
            self.request,
            self.result_template,
            {
                "change_details": self.calculated_changes,
                "num_modified": self.num_parent_objects,
                "num_failed": self.num_child_objects,
                "operation_mode": "remove",
                "next_url": self.next_url,
            },
        )

    def calculate_draft_tags(self, page, draft_tags, operation_mode):
        tags_to_remove = json.loads(self.request.POST.get("tags_to_remove", "{}"))
        codes_to_remove = tags_to_remove.get(str(page.id), [])
        return self._remove_tags(draft_tags, codes_to_remove)

    def calculate_changes(self, items):
        tags_to_remove = json.loads(self.request.POST.get("tags_to_remove", "{}"))
        changes = []

        for item in items:
            page = item["item"]
            page_id = str(page.id)
            original_tags = item.get("taxonomy_tags", [])

            codes_to_remove = tags_to_remove.get(page_id, [])
            final_tags = self._remove_tags(original_tags, codes_to_remove)
            _, _ = self._calculate_diff(original_tags, final_tags)

            changes.append(
                {
                    "item": page,
                    "tags": self._get_current_tags(page),
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
            current_tags = self._get_current_tags(item)
            new_tags = []

            for tag in current_tags:

                tag["status"] = (
                    "removed" if tag["code"] in tags_to_remove else "unchanged"
                )

                new_tags.append(tag)

            removed_count = len([t for t in new_tags if t["status"] == "removed"])

            return_items.append(
                {
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
            context["taxonomy_terms_json"] = taxonomy_data.terms_json
        except TaxonomyTerms.DoesNotExist:
            logger.error("Taxonomy terms not found")
            return []

    def calculate_draft_tags(self, page, draft_tags, operation_mode):
        tags_to_add = json.loads(self.request.POST.get("tags_to_add", "[]"))
        return self._merge_tags(draft_tags, tags_to_add, operation_mode)

    def calculate_changes(self, items):
        tags_to_add = json.loads(self.request.POST.get("tags_to_add", "[]"))
        operation_mode = self.request.POST.get("tag_operation_mode", "merge")
        changes = []

        for item in items:
            page = item["item"]
            original_tags = item.get("taxonomy_tags", [])
            final_tags = self._merge_tags(original_tags, tags_to_add, operation_mode)
            added, removed = self._calculate_diff(original_tags, final_tags)

            changes.append(
                {
                    "page_id": page.id,
                    "page_title": page.title,
                    "original_tags": json.loads(json.dumps(original_tags)),
                    "final_tags": final_tags,
                    "tags_added": added,
                    "tags_removed": removed,
                    "operation_mode": operation_mode,
                    "had_changes": bool(added or removed),
                }
            )

        return changes
