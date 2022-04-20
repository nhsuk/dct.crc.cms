from django import forms
from django.core.validators import EmailValidator, RegexValidator

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

CAMPAIGN_CHOICES = (
    ("", "Choose an option"),
    ("start4life", "Start4Life"),
    ("actfast", "Act FAST - Stroke"),
    ("nhshealthcheck", "NHS Health Check"),
    ("change4life", "Change4Life"),
    ("wintervaccinations", "Winter Vaccinations Public Facing Campaign"),
    ("schoolzone", "School Zone"),
    ("resourceordering", "Resource ordering"),
    ("keepantibioticsworking", "Keep Antibiotics Working"),
    ("toptipsteeth", "Top Tips for Teeth"),
    ("healthieryou", "Healthier You"),
    ("nhsrecruitment", "NHS Recruitment"),
    ("prescriptionexemptionchecking", "Check Before You Tick (Prescription Exemption Checking)"),
    ("change4lifenutrition", "Change4Life Nutrition Campaign"),
    ("cervicalscreening", "Cervical Screening campaign"),
    ("healthandsocialcareworkers", "Health and Social Care Workers Winter Vaccinations 2021"),
    ("weareundefeatable", "We Are Undefeatable"),
    ("reducinglenthofstay", "Reducing Length of Stay (RLOS)"),
    ("staywellthiswinter", "Stay Well This Winter"),
    ("nhsgeneralpracticeteam", "NHS General Practice Multidisciplinary Team"),
    ("dentalexemptionchecking", "Check before you tick (Dental Exemption Checking)"),
    ("coronavirus", "Coronavirus (COVID-19)"),
    ("foragreenernhs", "For a greener NHS"),
    ("betterhealth", "Better Health"),
    ("everymindmatters", "Better Health - Every Mind Matters"),
    ("helpushelpyoumaternity", "Help Us, Help You - Accessing NHS Services - Maternity"),
    ("helpushelpyoucancer", "Help Us Help You - Abdominal and Urological Symptoms of Cancer"),
    ("helpushelpyoumentalhealth", "Help Us, Help You - Accessing NHS Services - Mental Health"),
    ("nhs111winter", "NHS 111 Winter 2021/22"),
    ("helpushelpyoulungcancer", "Help Us Help You - Lung Cancer Symptoms"),
    ("heatwave", "Heatwave"),
    ("10minuteshakeup", "10 Minute Shake Up"),
    ("nhsaccess", "NHS Access - Staycation Assets"),
    ("stoptober2021", "Stoptober 2021"),
    ("localauthoritytier2", "Local Authority Tier 2 Adult Weight Management Programme Activation Guide &amp; Resources"),
    ("wearethenhs", "We are the NHS - International Recruitment - Nursing"),
    ("other", "Other"),
)

class ContactUsForm(forms.Form):

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
            },
            choices=JOB_CHOICES,
        ),
        required=True,
        error_messages={"required": "Select your job function"},
    )

    organisation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "organisation_name-error",
                "autocomplete": "organization",
            }
        ),
        required=True,
        error_messages={"required": "Enter your organisation name"},
    )

    organisation_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-describedby": "organisation_type-error",
            }
        ),
        required=True,
        error_messages={"required": "Enter your organisation type"},
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "aria-describedby": "email-error",
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "email",
            }
        ),
        validators=[EmailValidator(message="Enter an email address in the correct format")],
        error_messages={"required": "Enter your email address"},
    )

    healthy_behaviour = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "govuk-select",
                "onchange": "hideSelect();",
                "aria-describedby": " healthy_behaviour-error",
            },
            choices=CAMPAIGN_CHOICES,
        ),
        required=False,
    )

    other_campaign = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "disabled": True,
                "aria-describedby": "other_campaign-error",
            }
        ),
        required=False,
        error_messages={"required": "Enter other campaign"},
    )

    audience = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "aria-describedby": "audience-error",
                "rows": "5",
            }
        ),
        required=True,
        error_messages={"required": "Enter your audience"},
    )

    engage_audience = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "aria-describedby": "engage_audience-error",
                "rows": "5",
            }
        ),
        required=True,
        error_messages={"required": "Enter how you plan to engage this audience"},
    )

    product_service = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "aria-describedby": "product_service-error",
                "rows": "5",
            }
        ),
        required=False,
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "aria-describedby": "message-error",
                "rows": "5",
            }
        ),
        required=True,
        error_messages={"required": "Enter your message"},
    )

    class Meta:
        fields = [
            "first_name",
            "last_name",
            "job_title",
            "organisation",
            "organisation_type",
            "email",
            "healthy_behaviour",
            "other_campaign",
            "audience",
            "engage_audience",
            "product_service",
            "message",
        ]
