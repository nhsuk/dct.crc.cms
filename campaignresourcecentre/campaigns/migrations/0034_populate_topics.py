# Generated manually for CV-1396: Populate Topic model with initial topics

from django.db import migrations

INITIAL_TOPICS = [
    {"name": "Antimicrobial resistance", "code": "ANTMBREST"},
    {"name": "Cancer", "code": "CANCER"},
    {"name": "Childhood health", "code": "CHILDHOODHEALTH"},
    {"name": "Chronic illnesses", "code": "CHRONICILLNESSES"},
    {"name": "Dental health", "code": "DENTAL"},
    {"name": "Drinking less", "code": "DRINKING"},
    {"name": "Early diagnosis", "code": "EARLYDIAG"},
    {"name": "Early years", "code": "EARLYYEARS"},
    {"name": "Emergency care", "code": "EMERGENCYCARE"},
    {"name": "Maternity", "code": "MATERNITY"},
    {"name": "Mental health", "code": "MENTALHEALTH"},
    {"name": "NHS Services", "code": "NHSSERVICES"},
    {"name": "Physical activity", "code": "PHYSICALACTIVITY"},
    {"name": "Policy and brand guidelines", "code": "POLICYBRANDGUIDELINES"},
    {"name": "Quitting smoking", "code": "QUITTINGSMOKING"},
    {"name": "Recruitment", "code": "RECRUITMENT"},
    {"name": "Schools", "code": "SCHOOLS"},
    {"name": "Vaccinations", "code": "VACCINATIONS"},
    # Legacy topics carried over from taxonomies-list.json.
    # To be removed in CV-1410.
    {"name": "Blood pressure", "code": "BLOODPRESSURE", "show_in_filter": False},
    {"name": "Eating well", "code": "EATING", "show_in_filter": False},
    {"name": "Flu", "code": "FLU", "show_in_filter": False},
    {"name": "MMR", "code": "MMR", "show_in_filter": False},
    {"name": "NHS", "code": "NHS", "show_in_filter": False},
    {"name": "NHS 111", "code": "NHS111", "show_in_filter": False},
    {"name": "Screening", "code": "SCREENING", "show_in_filter": False},
    {"name": "Sepsis", "code": "SEPSIS", "show_in_filter": False},
]


def populate_topics(apps, schema_editor):
    """Populate the Topic model with initial topics for campaign/resource filters."""
    Topic = apps.get_model("campaigns", "Topic")

    for topic_data in INITIAL_TOPICS:
        Topic.objects.get_or_create(
            code=topic_data["code"],
            defaults={
                "name": topic_data["name"],
                "show_in_filter": topic_data.get("show_in_filter", True),
            },
        )


def reverse_populate_topics(apps, schema_editor):
    """Reverse migration - only remove the topics seeded by this migration."""
    Topic = apps.get_model("campaigns", "Topic")
    codes = [topic["code"] for topic in INITIAL_TOPICS]
    Topic.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0033_topic_code_and_show_in_filter"),
    ]

    operations = [
        migrations.RunPython(populate_topics, reverse_populate_topics),
    ]
