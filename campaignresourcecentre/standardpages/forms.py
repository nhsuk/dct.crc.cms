from django import forms
from django.core.validators import EmailValidator, RegexValidator

JOB_CHOICES = (
    ("", "Select a job function"),
    ("director", "Director / Board Member / CEO"),
    ("admin", "Administration"),
    ("education", "Education and Teaching"),
    ("marketing", "Marketing and communications"),
    ("hr", "HR / Training / Organisational Development"),
    ("community", "Community and Social Services / Charity / Volunteering"),
    ("student", "Student / Unemployed / Retired"),
    ("projectmanagement", "Project Management"),
    ("planning", "Planning and Development"),
    ("policy", "Policy"),
    ("environmental", "Environmental Health"),
    ("substance", "Substance Abuse and Addiction Services"),
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
    (
        "prescriptionexemptionchecking",
        "Check Before You Tick (Prescription Exemption Checking)",
    ),
    ("change4lifenutrition", "Change4Life Nutrition Campaign"),
    ("cervicalscreening", "Cervical Screening campaign"),
    (
        "healthandsocialcareworkers",
        "Health and Social Care Workers Winter Vaccinations 2021",
    ),
    ("weareundefeatable", "We Are Undefeatable"),
    ("reducinglenthofstay", "Reducing Length of Stay (RLOS)"),
    ("staywellthiswinter", "Stay Well This Winter"),
    ("nhsgeneralpracticeteam", "NHS General Practice Multidisciplinary Team"),
    ("dentalexemptionchecking", "Check before you tick (Dental Exemption Checking)"),
    ("coronavirus", "Coronavirus (COVID-19)"),
    ("foragreenernhs", "For a greener NHS"),
    ("betterhealth", "Better Health"),
    ("everymindmatters", "Better Health - Every Mind Matters"),
    (
        "helpushelpyoumaternity",
        "Help Us, Help You - Accessing NHS Services - Maternity",
    ),
    (
        "helpushelpyoucancer",
        "Help Us Help You - Abdominal and Urological Symptoms of Cancer",
    ),
    (
        "helpushelpyoumentalhealth",
        "Help Us, Help You - Accessing NHS Services - Mental Health",
    ),
    ("nhs111winter", "NHS 111 Winter 2021/22"),
    ("helpushelpyoulungcancer", "Help Us Help You - Lung Cancer Symptoms"),
    ("heatwave", "Heatwave"),
    ("10minuteshakeup", "10 Minute Shake Up"),
    ("nhsaccess", "NHS Access - Staycation Assets"),
    ("stoptober2021", "Stoptober 2021"),
    (
        "localauthoritytier2",
        "Local Authority Tier 2 Adult Weight Management Programme Activation Guide &amp; Resources",
    ),
    ("wearethenhs", "We are the NHS - International Recruitment - Nursing"),
    ("other", "Other"),
)


class ContactUsForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "given-name",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your first name"},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "family-name",
                "aria-required": "true",
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
                "autocomplete": "organization-title",
                "aria-required": "true",
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
                "autocomplete": "organization",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your organisation name"},
    )

    organisation_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your organisation type"},
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "govuk-input govuk-!-width-two-thirds",
                "autocomplete": "email",
                "aria-required": "true",
            }
        ),
        validators=[
            EmailValidator(message="Enter an email address in the correct format")
        ],
        error_messages={"required": "Enter your email address"},
    )

    healthy_behaviour = forms.CharField(
        widget=forms.Select(
            attrs={"class": "govuk-select", "onchange": "hideSelect();"},
            choices=CAMPAIGN_CHOICES,
        ),
        required=False,
    )

    other_campaign = forms.CharField(
        widget=forms.TextInput(attrs={"class": "govuk-input", "disabled": True}),
        required=False,
        error_messages={"required": "Enter other campaign"},
    )

    audience = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "rows": "5",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your audience"},
    )

    engage_audience = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "rows": "5",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter how you plan to engage this audience"},
    )

    product_service = forms.CharField(
        widget=forms.Textarea(attrs={"class": "govuk-textarea", "rows": "5"}),
        required=False,
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "govuk-textarea",
                "rows": "5",
                "aria-required": "true",
            }
        ),
        required=True,
        error_messages={"required": "Enter your message"},
    )

    # This is a hidden form field, only a spammer will fill it in.
    cat6a = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "govuk-visually-hidden",
                "aria-hidden": "true",
                "tabindex": -1,
            }
        ),
        required=False,
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
            "cat6a",
        ]
