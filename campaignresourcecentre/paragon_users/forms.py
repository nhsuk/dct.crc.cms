from django import forms
from django.core.validators import EmailValidator, RegexValidator

from campaignresourcecentre.paragon_users.helpers.validate_password import (
    validate_password_form,
)

JOB_CHOICES = (
    ("", "Select a job function"),
    ("director", "Director / Board Member / CEO"),
    ("admin", "Administration"),
    ("comms", "Communications"),
    ("education", "Education and Teaching"),
    ("marketing", "Marketing"),
    ("hr", "HR / Training / Organisational Development"),
    ("community", "Community and Social Services / Charity / Volunteering"),
    ("student", "Student / Unemployed / Retired"),
    ("health", "Health"),
    ("other", "Other"),
)


HEALTH_CHOICES = (
    ("health:other", "Other"),
    ("health:improvement", "Health Improvement / Public Health"),
    ("health:gpspecialistnurse", "GP, Specialist, Nurse and HCA"),
    ("health:pharmacy", "Pharmacy"),
    ("health:management", "Practice Management"),
)


ROLE_CHOICES = (
    ("", "Select a role"),
    ("Standard", "Standard"),
    ("Uber", "Uber"),
)


class RegisterForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "aria-describedby": "first_name-error",
                "autocomplete": "given-name",
            }
        ),
        required=True,
        error_messages={"required": "Enter your first name"},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "aria-describedby": "last_name-error",
                "autocomplete": "family-name",
            }
        ),
        required=True,
        error_messages={"required": "Enter your last name"},
    )

    job_title = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "govuk-select",
                "onchange": "hideSelect();",
                "aria-describedby": "job_title-error",
                "required": "False",
            },
            choices=JOB_CHOICES,
        ),
        required=False,
        error_messages={"required": "Select your job function"},
    )

    area_work = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "govuk-select",
                "disabled": False,
                "aria-describedby": "area_work-error"
            },
            choices=HEALTH_CHOICES,
        ),
        required=False,
        error_messages={"required": "Select an area of work"},
    )

    organisation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "organisation_name-error",
                "autocomplete": "organization",
            }
        ),
        required=False,
        error_messages={"required": "Enter your organisation name"},
    )

    postcode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-10",
                "aria-describedby": "postcode-error",
                "autocomplete": "postal-code",
            }
        ),
        required=True,
        error_messages={"required": "Enter your postcode"},
        validators=[
            RegexValidator(
                regex="^[A-Za-z]{1,2}[0-9]{1,2}[A-Za-z]?(\\s*[0-9][A-Za-z]{1,2})?$",
                message="Enter a valid postcode",
                code="invalid_postcode",
            )
        ],
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "aria-describedby": "email-error",
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": "Enter your email address"},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-input--width-10",
                "aria-describedby": "password-error",
                "autocomplete": "current-password",
            }
        ),
        validators=[validate_password_form],
        error_messages={"required": "Enter your password"},
    )

    terms = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "aria-describedby": "terms-error",
            }
        ),
        error_messages={"required": "Please accept the terms and conditions"},
        required=True,
    )

    class Meta:
        fields = [
            "email",
            "password",
            "email",
            "first_name",
            "last_name",
            "organisation",
            "job_title",
            "area_work",
            "postcode" "terms",
        ]


class UserAdminForm(forms.Form):
    user_token = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"disabled": "disabled"})
    )
    created_at = forms.DateTimeField(
        required=False, widget=forms.TextInput(attrs={"disabled": "disabled"})
    )
    verified_at = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"disabled": "disabled"})
    )
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    organisation = forms.CharField()
    job_title = forms.ChoiceField(
        choices=JOB_CHOICES,
    )
    area_work = forms.ChoiceField(
        required=False,
        choices=HEALTH_CHOICES,
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
    )
    postcode = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.all_fields_editable = kwargs.pop("all_fields_editable")
        super().__init__(*args, **kwargs)
        if not self.all_fields_editable:
            disabled_fields = (
                "email",
                "first_name",
                "last_name",
                "organisation",
                "job_title",
                "area_work",
                "postcode",
            )
            for field in disabled_fields:
                self.fields[field].required = False
                self.fields[field].widget.attrs.update({"disabled": "disabled"})

        if not self.initial["verified_at"]:
            self.initial["verified_at"] = "Not verified"

        job_title = self.initial["job_title"]
        if self.initial["job_title"] is not None:
            self.initial["job_title"] = job_title.split(":")[0]
        if self.initial["job_title"] == "health":
            self.initial["area_work"] = job_title


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocapitalize": "off",
                "class": "govuk-input",
                "aria-describedby": "email-error",
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": "Enter your email address"},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-one-half",
                "aria-describedby": "password-error",
                "autocomplete": "current-password",
            }
        ),
        error_messages={"required": "Enter your password"},
    )
    previous_page = forms.CharField(required=False)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocapitalize": "off",
                "class": "govuk-input",
                "aria-describedby": "email-error",
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": "Enter your email address"},
    )


class PasswordSetForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "aria-describedby": "password-error",
                "autocomplete": "new-password",
            }
        ),
        error_messages={"required": "Enter your password"},
        help_text="Password must contain at least one number, at least one capital letter and at least one symbol and must be more than 8 characters long.",  # noqa
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "aria-describedby": "password-check-error",
                "autocomplete": "new-password",
            }
        ),
        error_messages={"required": "Enter your password"},
    )


class AdminPasswordSetForm(PasswordSetForm):
    password_check = None


def checked_value(newsdict: dict, name: str):
    if newsdict.__len__ != 0 and newsdict.get(name):
        return "checked"
    else:
        return "checked"


class NewsLetterPreferencesForm(forms.Form):
    # Ages

    AllAges = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="All ages",
    )

    Pregnancyandyearold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="Pregnancy and 0 to 3 year old",
    )

    Childrenyearsold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="Children 3 to 11 years old",
    )

    Teensyearsold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="Teens 11 to 16 years old",
    )

    Adults = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="Adults",
    )

    OlderPeople = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "ages"}
        ),
        required=False,
        label="Older people (65 and over)",
    )

    # Themes
    AllThemes = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="All themes",
    )

    BecomingSmokefree = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Becoming Smokefree",
    )

    EatingWell = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Eating Well",
    )

    MovingMore = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Moving More",
    )

    CheckingYourselfSymptomAwareness = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Checking Yourself and Symptom Awareness",
    )

    DrinkingLess = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Drinking Less",
    )

    StressingLess = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Stressing Less",
    )

    SleepingWell = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "themes"}
        ),
        required=False,
        label="Sleeping Well",
    )

    # Subjects
    Allsubjects = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="All subjects",
    )

    Coronavirus = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Coronavirus (COVID-19)",
    )

    Flu = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Flu",
    )

    Stroke = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Stroke",
    )

    Cancer = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Cancer",
    )

    AntimicrobialResistance = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Antimicrobial Resistance",
    )

    SchoolsActivity = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Schools Activity",
    )

    SexualHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Sexual Health",
    )

    BloodPoisoningSepsis = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Sepsis",
    )

    NHSServices = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="NHS Services",
    )

    MaternityBreastFeeding = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Maternity and Breast Feeding",
    )

    Meningitis = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Meningitis",
    )

    DentalHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Dental Health",
    )

    MentalHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="Mental Health",
    )

    NHSandSocialCareFluLeads = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "govuk-checkboxes__input", "data-group": "subjects"}
        ),
        required=False,
        label="NHS and Social Care Flu Leads",
    )
