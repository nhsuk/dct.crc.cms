import json
from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _, ngettext
from wagtail.models import Page, PageQuerySet, PageManager
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from .utils import get_page_taxonomy_tags
from .forms import ManageTagsForm

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
        context['items'] = [
            {
                **item_data, 
                'taxonomy_tags': get_page_taxonomy_tags(
                    type(item_data['item']).objects.select_related().get(id=item_data['item'].id)
                )
            }
            for item_data in context.get('items', [])
        ]
        return context

    def get_execution_context(self):
        source_page = self.cleaned_form.cleaned_data.get('source_page')
        return {
            **super().get_execution_context(),
            'tags_to_remove': self.cleaned_form.cleaned_data.get('tags_to_remove', '{}'),
            'source_page_id': source_page.id if source_page else '',
            'tag_operation_mode': self.cleaned_form.cleaned_data.get('tag_operation_mode', 'merge'),
            'bulk_action_instance': self,
        }
    
    def form_valid(self, form):
        """Execute action and render results"""
        result = super().form_valid(form)
        
        # Get source page for results display
        source_page = self.cleaned_form.cleaned_data.get('source_page')
        source_page_obj = None
        if source_page:
            source_page_obj = source_page.specific
        
        # Determine operation type for smarter display
        tag_operation_mode = self.cleaned_form.cleaned_data.get('tag_operation_mode', 'merge')
        tags_to_remove = self.cleaned_form.cleaned_data.get('tags_to_remove', '{}')
        has_manual_removals = tags_to_remove and tags_to_remove != '{}'
        has_source_tags = source_page is not None
        
        # Determine display mode:
        # - 'comparison' if user manually removed tags (show removed vs added)
        # - 'old_new' if replace mode with source (show old vs new)
        # - 'final' if merge mode (show final tags only)
        if has_manual_removals:
            display_mode = 'comparison'
        elif tag_operation_mode == 'replace' and has_source_tags:
            display_mode = 'old_new'
        else:
            display_mode = 'final'
        
        return render(self.request, 'tag_management/results.html', {
            'change_details': self.change_details,
            'num_modified': self.num_parent_objects,
            'num_failed': self.num_child_objects,
            'source_page': source_page_obj,
            'tag_operation_mode': tag_operation_mode,
            'display_mode': display_mode,
            'next_url': self.next_url,
        })

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
            return get_page_taxonomy_tags(source_page)
        except (Page.DoesNotExist, ValueError):
            return []

    @classmethod
    def _update_page_taxonomy(cls, page, tags_to_remove_dict, source_tags, tag_operation_mode, user, bulk_action_instance=None):
        """Update taxonomy and track changes"""
        # Refresh from DB to ensure we have latest data
        page.refresh_from_db()
        page_specific = page.specific
        page_specific.refresh_from_db()
        
        current_taxonomy = get_page_taxonomy_tags(page_specific)
        original_taxonomy = current_taxonomy.copy()  # Track original state
        
        tags_removed = []
        tags_added = []
        
        # Handle replace mode - clear all existing tags if we're adding from source
        if tag_operation_mode == 'replace' and source_tags:
            tags_removed = current_taxonomy.copy()
            current_taxonomy = []
        
        # Remove specific tags
        page_id_str = str(page.id)
        if page_id_str in tags_to_remove_dict:
            codes_to_remove = tags_to_remove_dict[page_id_str]
            removed_tags = [tag for tag in current_taxonomy if tag.get('code') in codes_to_remove]
            if tag_operation_mode != 'replace' or not source_tags:  # Only track if not already cleared by replace
                tags_removed.extend(removed_tags)
            current_taxonomy = [tag for tag in current_taxonomy if tag.get('code') not in codes_to_remove]
        
        # Add tags from source
        if source_tags:
            existing_codes = {tag.get('code') for tag in current_taxonomy}
            new_tags = [tag for tag in source_tags if tag.get('code') not in existing_codes]
            tags_added = new_tags
            current_taxonomy.extend(new_tags)
        
        # Remove duplicates by code (just in case)
        seen_codes = set()
        deduplicated_taxonomy = []
        for tag in current_taxonomy:
            code = tag.get('code')
            if code and code not in seen_codes:
                seen_codes.add(code)
                deduplicated_taxonomy.append(tag)
        current_taxonomy = deduplicated_taxonomy
        
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
            'original_tags': original_taxonomy,
            'final_tags': current_taxonomy,
            'tags_removed': tags_removed,
            'tags_added': tags_added,
            'had_changes': bool(tags_removed or tags_added),
            'operation_mode': tag_operation_mode
        }
        
        if bulk_action_instance and change_detail['had_changes']:
            bulk_action_instance.change_details.append(change_detail)
        
        return change_detail['had_changes']

    @classmethod
    def execute_action(cls, objects, tags_to_remove='{}', source_page_id='', tag_operation_mode='merge', user=None, bulk_action_instance=None, **kwargs):
        tags_to_remove_dict = cls._parse_tags_to_remove(tags_to_remove)
        source_tags = cls._get_source_page_tags(source_page_id)
        
        num_modified = 0
        num_failed = 0
        
        for page in objects:
            try:
                if cls._update_page_taxonomy(page, tags_to_remove_dict, source_tags, tag_operation_mode, user, bulk_action_instance):
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
