from django import forms
from wagtail.admin.widgets import AdminPageChooser
from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from wagtail.models import Page


class ManageTagsForm(forms.Form):
    active_tab = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial="remove"
    )
    tags_to_remove = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial="{}"
    )
    tag_operation_mode = forms.ChoiceField(
        choices=[
            ("merge", "Merge Tags (add to existing tags)"),
            ("replace", "Replace Tags (remove existing tags first)"),
        ],
        initial="merge",
        widget=forms.RadioSelect,
        label="Tag Operation Mode",
        required=False,
    )
    source_page = forms.ModelChoiceField(
        queryset=Page.objects.none(),
        required=False,
        widget=AdminPageChooser(target_models=[CampaignPage, ResourcePage]),
        label="Select Source Resource/Campaign",
        help_text="Choose a page to copy tags from",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["source_page"].queryset = Page.objects.type(
            CampaignPage, ResourcePage
        ).all()
