import json
from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage


class ManageTagsForm(forms.Form):
    tags_to_remove = forms.CharField(widget=forms.HiddenInput(), required=False, initial='{}')
    source_page = forms.CharField(widget=forms.HiddenInput(), required=False)


class ManageTagsBulkAction(PageBulkAction):
    display_name = _("Manage Tags")
    aria_label = _("Manage tags for selected pages")
    action_type = "manage_tags"
    template_name = "tag_management/bulk_manage_tags.html"
    action_priority = 20
    models = [Page]
    form_class = ManageTagsForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_details = []

    def check_perm(self, page):
        return isinstance(page.specific, (CampaignPage, ResourcePage))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Force fresh DB query with no caching to avoid stale data
        from django.db import connection
        context['items'] = [
            {
                **item_data, 
                'taxonomy_tags': self._parse_page_taxonomy(
                    type(item_data['item']).objects.select_related().get(id=item_data['item'].id)
                )
            }
            for item_data in context.get('items', [])
        ]
        return context

    def get_execution_context(self):
        return {
            **super().get_execution_context(),
            'tags_to_remove': self.cleaned_form.cleaned_data.get('tags_to_remove', '{}'),
            'source_page_id': self.cleaned_form.cleaned_data.get('source_page', ''),
            'bulk_action_instance': self,
        }
    
    def form_valid(self, form):
        """Execute action and render results"""
        result = super().form_valid(form)
        
        # Get source page for results display
        source_page_id = self.cleaned_form.cleaned_data.get('source_page', '')
        source_page = None
        if source_page_id:
            try:
                source_page = Page.objects.get(id=source_page_id).specific
            except Page.DoesNotExist:
                pass
        
        return render(self.request, 'tag_management/results.html', {
            'change_details': self.change_details,
            'num_modified': self.num_parent_objects,
            'num_failed': self.num_child_objects,
            'source_page': source_page,
            'next_url': self.next_url,
        })

    @staticmethod
    def _parse_page_taxonomy(page):
        if not hasattr(page, 'taxonomy_json') or not page.taxonomy_json:
            return []
        try:
            taxonomy_data = json.loads(page.taxonomy_json)
            return taxonomy_data if isinstance(taxonomy_data, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    @staticmethod
    def _parse_tags_to_remove(tags_to_remove_json):
        try:
            return json.loads(tags_to_remove_json)
        except (json.JSONDecodeError, TypeError):
            return {}

    @classmethod
    def _get_source_page_tags(cls, source_page_id):
        if not source_page_id:
            return []
        try:
            source_page = Page.objects.get(id=source_page_id).specific
            return cls._parse_page_taxonomy(source_page)
        except (Page.DoesNotExist, ValueError):
            return []

    @classmethod
    def _update_page_taxonomy(cls, page, tags_to_remove_dict, source_tags, user, bulk_action_instance=None):
        """Update taxonomy and track changes"""
        # Refresh from DB to ensure we have latest data
        page.refresh_from_db()
        page_specific = page.specific
        page_specific.refresh_from_db()
        
        current_taxonomy = cls._parse_page_taxonomy(page_specific)
        
        tags_removed = []
        tags_added = []
        
        # Remove tags
        page_id_str = str(page.id)
        if page_id_str in tags_to_remove_dict:
            codes_to_remove = tags_to_remove_dict[page_id_str]
            tags_removed = [tag for tag in current_taxonomy if tag.get('code') in codes_to_remove]
            current_taxonomy = [tag for tag in current_taxonomy if tag.get('code') not in codes_to_remove]
        
        # Add tags
        if source_tags:
            existing_codes = {tag.get('code') for tag in current_taxonomy}
            tags_added = [tag for tag in source_tags if tag.get('code') not in existing_codes]
            current_taxonomy.extend(tags_added)
        
        # Save with revision history
        page_specific.taxonomy_json = json.dumps(current_taxonomy)
        
        # Save the page object first to update the database
        page_specific.save()
        
        # Then create revision for history
        revision = page_specific.save_revision(
            user=user,
            log_action=True,
            changed=bool(tags_removed or tags_added)
        )
        
        # If page is live, publish the revision to ensure it's reflected
        if page.live:
            revision.publish(user=user)
        
        # Force refresh after save to clear any caches
        page.refresh_from_db()
        page_specific.refresh_from_db()
        
        # Track for results
        change_detail = {
            'page_id': page.id,
            'page_title': page.title,
            'tags_removed': tags_removed,
            'tags_added': tags_added,
            'had_changes': bool(tags_removed or tags_added)
        }
        
        if bulk_action_instance and change_detail['had_changes']:
            bulk_action_instance.change_details.append(change_detail)
        
        return change_detail['had_changes']

    @classmethod
    def execute_action(cls, objects, tags_to_remove='{}', source_page_id='', user=None, bulk_action_instance=None, **kwargs):
        tags_to_remove_dict = cls._parse_tags_to_remove(tags_to_remove)
        source_tags = cls._get_source_page_tags(source_page_id)
        
        num_modified = 0
        num_failed = 0
        
        for page in objects:
            try:
                if cls._update_page_taxonomy(page, tags_to_remove_dict, source_tags, user, bulk_action_instance):
                    num_modified += 1
            except Exception as e:
                if bulk_action_instance:
                    bulk_action_instance.change_details.append({
                        'page_id': page.id,
                        'page_title': page.title,
                        'error': str(e),
                        'had_changes': False
                    })
                num_failed += 1
        
        return num_modified, num_failed

    def get_success_message(self, num_parent_objects, num_child_objects):
        if num_child_objects > 0:
            return _("%(num_modified)d pages updated. %(num_failed)d failed.") % {
                "num_modified": num_parent_objects, "num_failed": num_child_objects
            }
        return ngettext(
            "%(num_modified)d page updated",
            "%(num_modified)d pages updated",
            num_parent_objects,
        ) % {"num_modified": num_parent_objects}
