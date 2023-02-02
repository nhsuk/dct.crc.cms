from django import forms

from campaignresourcecentre.paragon_users.forms import validate_postcode


class DeliveryAddressForm(forms.Form):
    Address1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "aria-describedby": "full_name-error",
                "autocomplete": "name",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your full name"},
    )

    Address2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "address_line_1-error",
                "autocomplete": "address-line1",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your address line 1"},
    )

    Address3 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "address_line_2-error",
                "autocomplete": "address-line2",
            }
        ),
        required=False,
        error_messages={"required": "Enter your address line 2"},
    )

    Address4 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "town_or_city-error",
                "autocomplete": "address-level1",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your town or city"},
    )

    Address5 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-10",
                "aria-describedby": "postcode-error",
                "autocomplete": "postal-code",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your postcode"},
        validators=[validate_postcode],
    )

    class Meta:
        fields = ["Address1", "Address2", "Address3", "Address4", "Address5"]
