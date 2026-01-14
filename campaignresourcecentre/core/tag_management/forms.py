from django import forms
from wagtail.admin.widgets import AdminPageChooser
from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from wagtail.models import Page

class CopyTaxonomyTagsForm(forms.Form):
    """Form for copying tags from one page to another"""
    tag_operation_mode = forms.ChoiceField(
        choices=[
            ('merge', 'Merge Tags (add to existing tags)'),
            ('replace', 'Replace Tags (remove existing tags first)'),
        ],
        initial='merge',
        widget=forms.RadioSelect,
        label="Tag Operation Mode",
        required=True,
    )

    source_page = forms.ModelChoiceField(
        queryset=Page.objects.type(CampaignPage, ResourcePage).all(),
        required=True,
        widget=AdminPageChooser(target_models=[CampaignPage, ResourcePage]),
        label="Select Source Resource/Campaign",
        help_text="Choose a page to copy tags from"
    )

    def __init__(self, *args, exclude_page_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = self.fields['source_page'].queryset
        if exclude_page_id:
            queryset = queryset.exclude(id=exclude_page_id)
        self.fields['source_page'].queryset = queryset

class ManageTagsForm(forms.Form):
    tags_to_remove = forms.CharField(widget=forms.HiddenInput(), required=False, initial='{}')
    source_page = forms.ModelChoiceField(
        queryset=Page.objects.type(CampaignPage, ResourcePage).all(),
        required=False,
        widget=AdminPageChooser(target_models=[CampaignPage, ResourcePage]),
        label="Select Source Resource/Campaign",
        help_text="Choose a page to copy tags from"
    )
    tag_operation_mode = forms.ChoiceField(
        choices=[
            ('merge', 'Merge Tags (add to existing tags)'),
            ('replace', 'Replace Tags (remove existing tags first)'),
        ],
        initial='merge',
        widget=forms.RadioSelect,
        label="Tag Operation Mode",
        required=False,
    )
