from django import forms


class ManageTagsForm(forms.Form):
    tags_to_remove = forms.CharField(
        widget=forms.Textarea(attrs={"hidden": True}), required=False,
    )
    tags_to_add = forms.CharField(
        widget=forms.Textarea(attrs={"hidden": True}), required=False
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
