import json
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.wagtailreacttaxonomy.models import TaxonomyTerms
from .utils import get_page_taxonomy_tags
from .forms import ManageTagsForm
from wagtail import hooks


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


class ManageTagsBulkAction(PageBulkAction):
    models = [Page]
    form_class = ManageTagsForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculated_changes = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = [
            {**item, "taxonomy_tags": get_page_taxonomy_tags(item["item"].specific)}
            for item in context.get("items", [])
        ]
        return context

    def check_perm(self, page):
        if page.alias_of_id:
            return False
        return isinstance(page.specific, (CampaignPage, ResourcePage))

    def calculate_changes(self, items):
        raise NotImplementedError("Subclasses must implement calculate_changes")

    def apply_changes(self, user):
        num_modified = 0
        num_failed = 0

        for change in self.calculated_changes:
            if not change.get("had_changes"):
                continue

            try:
                page = Page.objects.get(id=change["page_id"])

                if page.alias_of_id:
                    change["error"] = "Cannot modify alias pages"
                    change["had_changes"] = False
                    num_failed += 1
                    continue

                self._save_tags(page, change["final_tags"], user)
                num_modified += 1
            except Exception as e:
                change["error"] = str(e)
                change["had_changes"] = False
                num_failed += 1

        return num_modified, num_failed

    def _save_tags(self, page, tags, user):
        if page.alias_of_id:
            raise ValueError("Cannot modify tags on alias pages")

        page_specific = page.specific
        page_specific.taxonomy_json = json.dumps(tags)
        page_specific.save()
        revision = page_specific.save_revision(
            user=user,
            log_action=self.action_type,
            changed=True,
        )
        if page.live:
            revision.publish(user=user)

    def post(self, request, *args, **kwargs):
        if request.POST.get("next_action") == "go_back":
            ctx = self.get_context_data(**kwargs)
            ctx["form"] = self.form_class(request.POST or None)
            return self.render_to_response(ctx)

        if request.POST.get("next_action") == "preview_changes":
            ctx = self.get_context_data(**kwargs)
            self.calculated_changes = self.calculate_changes(ctx.get("items", []))
            ctx["preview_changes"] = True
            ctx["items"] = [
                {**item, **change}
                for item, change in zip(ctx["items"], self.calculated_changes)
            ]
            ctx["calculated_changes_json"] = json.dumps(self.calculated_changes)
            ctx["operation_mode"] = request.POST.get("tag_operation_mode", "merge")
            return self.render_to_response(ctx)

        if request.POST.get("next_action") == "apply_changes" and request.POST.get(
            "calculated_changes"
        ):
            try:
                self.calculated_changes = json.loads(
                    request.POST.get("calculated_changes")
                )
            except (json.JSONDecodeError, TypeError):
                self.calculated_changes = []

        return super().post(request, *args, **kwargs)

    def get_execution_context(self):
        return {
            **super().get_execution_context(),
            "bulk_action_instance": self,
        }

    @classmethod
    def execute_action(cls, objects, **kwargs):
        instance = kwargs.get("bulk_action_instance")
        user = kwargs.get("user")

        if not instance:
            return 0, len(objects)

        if (
            not hasattr(instance, "calculated_changes")
            or not instance.calculated_changes
        ):
            return 0, len(objects)

        return instance.apply_changes(user)

    def get_success_message(self, num_parent_objects, num_child_objects):
        """Return success message showing how many pages were modified."""
        if num_parent_objects > 0:
            return ngettext(
                "%(num_parent_objects)d page has been updated successfully.",
                "%(num_parent_objects)d pages have been updated successfully.",
                num_parent_objects,
            ) % {"num_parent_objects": num_parent_objects}
        return _("No pages were modified.")

    def form_valid(self, form):
        super().form_valid(form)

        return render(
            self.request,
            self.result_template,
            {
                "change_details": self.calculated_changes,
                "num_modified": self.num_parent_objects,
                "num_failed": self.num_child_objects,
                "operation_mode": form.cleaned_data.get("tag_operation_mode", "merge"),
                "next_url": self.next_url,
            },
        )


class RemoveTagsBulkAction(ManageTagsBulkAction):
    template_name = "tag_management/remove-tags-form.html"
    result_template = "tag_management/results.html"
    display_name = _("Remove Tags")
    aria_label = _("Remove tags from selected pages")
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

    def calculate_changes(self, items):
        tags_to_remove = json.loads(self.request.POST.get("tags_to_remove", "{}"))
        changes = []

        for item in items:
            page = item["item"]
            page_id = str(page.id)

            original_tags = item.get("taxonomy_tags", [])

            if page_id in tags_to_remove:
                codes_to_remove = set(tags_to_remove[page_id])
                removed = [t for t in original_tags if t.get("code") in codes_to_remove]
                final_tags = [
                    t for t in original_tags if t.get("code") not in codes_to_remove
                ]
            else:
                removed = []
                final_tags = original_tags

            changes.append(
                {
                    "page_id": page.id,
                    "page_title": page.title,
                    "original_tags": json.loads(json.dumps(original_tags)),
                    "final_tags": final_tags,
                    "tags_removed": removed,
                    "tags_added": [],
                    "had_changes": bool(removed),
                }
            )

        return changes


class AddTagsBulkAction(ManageTagsBulkAction):
    display_name = _("Add Tags")
    aria_label = _("Add tags to selected pages")
    action_type = "add_tags"
    template_name = "tag_management/add-tags-form.html"
    result_template = "tag_management/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            taxonomy_data = TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy")
            context["taxonomy_terms_json"] = taxonomy_data.terms_json
        except TaxonomyTerms.DoesNotExist:
            context["taxonomy_terms_json"] = "[]"
            context["taxonomy_error"] = "Taxonomy terms not found"
        return context

    def calculate_changes(self, items):
        tags_to_add = json.loads(self.request.POST.get("tags_to_add", "[]"))
        operation_mode = self.request.POST.get("tag_operation_mode", "merge")
        changes = []

        for item in items:
            page = item["item"]
            original_tags = item.get("taxonomy_tags", [])

            if operation_mode == "replace":
                final_tags = tags_to_add.copy()
                removed = original_tags.copy()
                added = tags_to_add.copy()
            else:
                existing_codes = {t.get("code") for t in original_tags}
                added = [t for t in tags_to_add if t.get("code") not in existing_codes]
                final_tags = original_tags + added
                removed = []

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
