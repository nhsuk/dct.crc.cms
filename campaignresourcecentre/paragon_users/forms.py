from logging import getLogger

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.utils.regex_helper import _lazy_re_compile

from campaignresourcecentre.paragon_users.helpers.postcodes import get_postcode_region
from campaignresourcecentre.paragon_users.helpers.validate_password import (
    validate_password_form,
)

logger = getLogger(__name__)

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
    ("health:pharmacy", "Pharmacy"),
    ("health:nurse", "Nurse"),
    ("health:management", "Practice Management"),
    ("health:infantteam", "Infant feeding team"),
    ("health:childrensteam", "Childrens centre team"),
    ("health:oralhealth", "Oral health"),
    ("health:improvement", "Health Improvement / Public Health"),
    ("health:healthvisitor", "Health visitor"),
    ("health:gp", "GP"),
    ("health:midwife", "Midwife"),
    ("health:smokingcessation", "Smoking cessation"),
    ("health:healthwellbeing", "Health and Wellbeing coach"),
    ("health:healthassistant", "Health Care Assistant"),
    ("health:socialprescribing", "Social Prescribing Link Worker"),
    ("health:carecoordinator", "Care Coordinator"),
    ("health:immunisation", "Immunisation Coordinator"),
    ("health:other", "Other"),
)


ROLE_CHOICES = (("", "Select a role"), ("standard", "Standard"), ("uber", "Uber"))

ENTER_EMAIL = "Enter your email address"
ENTER_PASSWORD = "Enter your password"

DESELECTALL_AGES = "DeselectAllOption(this,'Ages')"
DESELECTALL_THEMES = "DeselectAllOption(this,'Themes')"
DESELECTALL_SUBJECTS = "DeselectAllOption(this,'Subjects')"


# uses regex to restrict usage of everything but a expression of allowed characters
class SpecialCharacterRestrictionValidator(RegexValidator):
    regex = "^[a-zA-Z0-9\\-' ]*$"
    field_name = "this field"
    message = "The only special characters you can use in {} are a hyphen (-) and an apostrophe (')".format(
        field_name
    )

    def __init__(self, field_name):
        if field_name is not None:
            self.field_name = field_name
        self.regex = _lazy_re_compile(self.regex, self.flags)


# uses get_postcode_region to verify existence of specified postcode
def validate_postcode(postcode):
    try:
        get_postcode_region(postcode)
    except Exception as e:
        logger.warn("Failed to verify postcode '%s' (%s)", postcode, e)
        raise ValidationError(
            "Postcode '%(postcode)s' not recognised", params={"postcode": postcode}
        )


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "given-name",
                "aria-describedby": "first_name-error",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your first name"},
        validators=[
            SpecialCharacterRestrictionValidator(field_name="the first name field")
        ],
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "family-name",
                "aria-describedby": "last_name-error",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your last name"},
        validators=[
            SpecialCharacterRestrictionValidator(field_name="the last name field")
        ],
    )

    job_title = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "govuk-select",
                "onchange": "hideSelect();",
                "autocomplete": "organization-title",
                "aria-describedby": "job_title-error",
                "aria-required": "true",
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
                "aria-describedby": "area_work-error",
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
                "autocomplete": "organization",
                "aria-describedby": "organisation_name-error",
            }
        ),
        required=False,
        error_messages={"required": "Enter your organisation name"},
        validators=[
            SpecialCharacterRestrictionValidator(
                field_name="the organisation name field"
            )
        ],
    )

    postcode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-10",
                "autocomplete": "postal-code",
                "aria-describedby": "postcode-error",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your postcode"},
        validators=[validate_postcode],
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "email",
                "aria-describedby": "email-error",
                "aria-required": "true",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": ENTER_EMAIL},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-input--width-10",
                "autocomplete": "current-password",
                "aria-describedby": "helper-text password-error",
            }
        ),
        validators=[validate_password_form],
        error_messages={"required": ENTER_PASSWORD},
    )

    terms = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "aria-describedby": "terms-error",
                "aria-required": "true",
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
            "postcode",
            "terms",
        ]


class EmailUpdatesForm(forms.Form):
    EMAIL_UPDATES_CHOICES = (
        ("yes", "Get email updates"),
        ("no", "I do not want email updates"),
    )
    email_updates = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "govuk-radios__input"}),
        choices=EMAIL_UPDATES_CHOICES,
        required=True,
        error_messages={"required": "Select an option"},
    )


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
    job_title = forms.ChoiceField(choices=JOB_CHOICES)
    area_work = forms.ChoiceField(required=False, choices=HEALTH_CHOICES)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
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
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": ENTER_EMAIL},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-one-half",
                "autocomplete": "current-password",
            }
        ),
        error_messages={"required": ENTER_PASSWORD},
    )
    previous_page = forms.CharField(required=False)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocapitalize": "off",
                "class": "govuk-input",
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator],
        error_messages={"required": ENTER_EMAIL},
    )


class PasswordSetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-one-half",
                "autocomplete": "new-password",
            }
        ),
        error_messages={"required": ENTER_PASSWORD},
        validators=[validate_password_form],
        help_text="Password must contain at least one number, at least one capital letter and at least one symbol and must be more than 8 characters long.",  # noqa
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "govuk-input govuk-!-width-one-half",
                "autocomplete": "new-password",
            }
        ),
        error_messages={"required": ENTER_PASSWORD},
    )


class AdminPasswordSetForm(PasswordSetForm):
    password_check = None


class NewsLetterPreferencesForm(forms.Form):
    # Ages

    AllAges = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": "SelectAll(this,'ages')",
            }
        ),
        required=False,
        label="All ages",
    )

    Pregnancyandyearold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": DESELECTALL_AGES,
            }
        ),
        required=False,
        label="Pregnancy and 0 to 3 year old",
    )

    Childrenyearsold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": DESELECTALL_AGES,
            }
        ),
        required=False,
        label="Children 3 to 11 years old",
    )

    Teensyearsold = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": DESELECTALL_AGES,
            }
        ),
        required=False,
        label="Teens 11 to 16 years old",
    )

    Adults = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": DESELECTALL_AGES,
            }
        ),
        required=False,
        label="Adults",
    )

    OlderPeople = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "ages",
                "onclick": DESELECTALL_AGES,
            }
        ),
        required=False,
        label="Older people (65 and over)",
    )

    # Themes
    AllThemes = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": "SelectAll(this,'themes')",
            }
        ),
        required=False,
        label="All health behaviours",
    )

    BecomingSmokefree = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Becoming Smokefree",
    )

    EatingWell = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Eating Well",
    )

    MovingMore = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Moving More",
    )

    CheckingYourselfSymptomAwareness = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Checking Yourself and Symptom Awareness",
    )

    DrinkingLess = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Drinking Less",
    )

    StressingLess = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Stressing Less",
    )

    SleepingWell = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "themes",
                "onclick": DESELECTALL_THEMES,
            }
        ),
        required=False,
        label="Sleeping Well",
    )

    # Subjects
    AllSubjects = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": "SelectAll(this,'subjects')",
            }
        ),
        required=False,
        label="All topics",
    )

    Coronavirus = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Coronavirus (COVID-19)",
    )

    Flu = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Flu",
    )

    Stroke = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Stroke",
    )

    Cancer = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Cancer",
    )

    AntimicrobialResistance = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Antimicrobial Resistance",
    )

    SchoolsActivity = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Schools Activity",
    )

    SexualHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Sexual Health",
    )

    BloodPoisoningSepsis = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Sepsis",
    )

    NHSServices = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="NHS Services",
    )

    MaternityBreastFeeding = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Maternity and Breast Feeding",
    )

    Meningitis = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Meningitis",
    )

    DentalHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Dental Health",
    )

    MentalHealth = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="Mental Health",
    )

    NHSandSocialCareFluLeads = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "govuk-checkboxes__input",
                "data-group": "subjects",
                "onclick": DESELECTALL_SUBJECTS,
            }
        ),
        required=False,
        label="NHS and Social Care Flu Leads",
    )
