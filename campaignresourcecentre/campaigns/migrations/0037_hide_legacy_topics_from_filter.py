# Hide legacy topics from the campaigns filter.
# These topics are carried over from the old taxonomies-list.json and will be fully removed in CV-1410.

from django.db import migrations

LEGACY_TOPIC_CODES = [
    "BLOODPRESSURE",
    "EATING",
    "FLU",
    "MMR",
    "NHS",
    "NHS111",
    "SCREENING",
    "SEPSIS",
]


def hide_legacy_topics(apps, schema_editor):
    Topic = apps.get_model("campaigns", "Topic")
    Topic.objects.filter(code__in=LEGACY_TOPIC_CODES).update(show_in_filter=False)


def show_legacy_topics(apps, schema_editor):
    Topic = apps.get_model("campaigns", "Topic")
    Topic.objects.filter(code__in=LEGACY_TOPIC_CODES).update(show_in_filter=True)


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0036_topic_show_in_filter"),
    ]

    operations = [
        migrations.RunPython(hide_legacy_topics, show_legacy_topics),
    ]
