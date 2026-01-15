import json
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from .utils import get_page_taxonomy_tags
from .forms import ManageTagsForm


class ManageTagsBulkAction(PageBulkAction):
    """Base class for tag management bulk actions."""

    models = [Page]
    form_class = ManageTagsForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_details = []
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = [
            {**item, "taxonomy_tags": get_page_taxonomy_tags(item["item"].specific)}
            for item in context.get("items", [])
        ]
        return context

    def check_perm(self, page):
        return isinstance(page.specific, (CampaignPage, ResourcePage))

    def get_execution_context(self):
        cleaned_data = self.cleaned_form.cleaned_data
        return {
            **super().get_execution_context(),
            "tags_to_remove": cleaned_data.get("tags_to_remove", "{}"),
            "source_page_id": (
                cleaned_data.get("source_page").id
                if cleaned_data.get("source_page")
                else None
            ),
            "tag_operation_mode": cleaned_data.get("tag_operation_mode", "merge"),
            "bulk_action_instance": self,
        }

    def form_valid(self, form):
        super().form_valid(form)

        return render(
            self.request,
            self.result_template,
            {
                "change_details": self.change_details,
                "num_modified": self.num_parent_objects,
                "num_failed": self.num_child_objects,
                "operation_mode": self.cleaned_form.cleaned_data.get("tag_operation_mode", "merge"),
                "next_url": self.next_url,
            },
        )

    @staticmethod
    def save_page_tags(page, tags, user):
        page_specific = page.specific
        page_specific.taxonomy_json = json.dumps(tags)
        page_specific.save()
        revision = page_specific.save_revision(user=user, log_action=True, changed=True)
        if page.live:
            revision.publish(user=user)

    @staticmethod
    def track_changes(
        instance, page, original, final, removed, added, mode, had_changes=True
    ):
        if instance:
            instance.change_details.append(
                {
                    "page_id": page.id,
                    "page_title": page.title,
                    "page_url": page.specific.url if hasattr(page, "specific") else "",
                    "edit_url": getattr(
                        page, "edit_url", f"/crc-admin/pages/{page.id}/edit/"
                    ),
                    "original_tags": original,
                    "final_tags": final,
                    "tags_removed": removed,
                    "tags_added": added,
                    "operation_mode": mode,
                    "had_changes": had_changes,
                }
            )

    @classmethod
    def execute_action(cls, objects, **kwargs):
        instance = kwargs.get("bulk_action_instance")
        num_modified = 0
        num_failed = 0
        
        for page in objects:
            try:
                cls.process_page(page, **kwargs)
                num_modified += 1
            except Exception as e:
                if instance:
                    instance.change_details.append(
                        {
                            "page_id": page.id,
                            "page_title": page.title,
                            "edit_url": getattr(
                                page,
                                "edit_url",
                                f"/crc-admin/pages/{page.id}/edit/",
                            ),
                            "error": str(e),
                        }
                    )
                num_failed += 1
        return num_modified, num_failed

    def get_success_message(self, num_modified, num_failed):
        if num_failed:
            return _(f"{num_modified} pages updated. {num_failed} failed.")
        return ngettext(
            f"{num_modified} page updated",
            f"{num_modified} pages updated",
            num_modified,
        )
        
    @classmethod
    def process_page(cls, page, **kwargs):
        raise NotImplementedError("Subclasses must implement process_page method.")

class RemoveTagsBulkAction(ManageTagsBulkAction):
    """Bulk action to remove tags from selected pages."""

    template_name = "tag_management/remove-tags-form.html"
    display_name = _("Remove Tags")
    aria_label = _("Remove tags from selected pages")
    action_type = "remove_tags"
    result_template = "tag_management/results.html"
    
    @classmethod
    def remove_tags_from_page(cls, page, tags_to_remove, user, instance=None):
        if str(page.id) not in tags_to_remove:
            return False

        current = get_page_taxonomy_tags(page.specific)
        codes = tags_to_remove[str(page.id)]
        removed = [t for t in current if t.get("code") in codes]
        final = [t for t in current if t.get("code") not in codes]

        if not removed:
            return False

        cls.save_page_tags(page, final, user)
        cls.track_changes(instance, page, current, final, removed, [], "remove")
        return True
    
    @classmethod
    def process_page(cls, page, tags_to_remove="{}", user=None, **kwargs):
        instance = kwargs.get('bulk_action_instance')
        tags_dict = json.loads(tags_to_remove) if tags_to_remove else {}
        return cls.remove_tags_from_page(page, tags_dict, user, instance)


class CopyTagsBulkAction(ManageTagsBulkAction):
    """Bulk action to copy tags from another resource to selected pages."""

    display_name = _("Copy Tags from Another Resource")
    aria_label = _("Copy tags from another resource to selected pages")
    action_type = "copy_tags"
    result_template = "tag_management/results.html"
    template_name = "tag_management/copy-tags-form.html"

    @classmethod
    def process_page(
        cls,
        page,
        source_page_id=None,
        tag_operation_mode="merge",
        user=None,
        **kwargs,
    ):
        instance = kwargs.get('bulk_action_instance')
        source_tags = get_page_taxonomy_tags(Page.objects.get(id=source_page_id).specific)
        current_tags = get_page_taxonomy_tags(page.specific)
        
        if tag_operation_mode == "replace":
            final = source_tags.copy()
            removed = current_tags.copy()
            added = source_tags.copy()
        else:
            existing = {t.get("code") for t in current_tags}
            added = [t for t in source_tags if t.get("code") not in existing]
            final = current_tags + added
            removed = []

        had_changes = bool(added or removed)

        if had_changes:
            cls.save_page_tags(page, final, user)

        cls.track_changes(
            instance, page, current_tags, final, removed, added, tag_operation_mode, had_changes
        )
        
        return had_changes
        