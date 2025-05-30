# Generated by Django 5.0.14 on 2025-05-19 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0004_systemmessagessettings_banner_enabled_and_more"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeatureFlags",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sz_email_variant",
                    models.BooleanField(
                        default=False,
                        help_text="Enable or disable the School Zone email signup journey feature flag",
                        verbose_name="School Zone email journey",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feature Flags",
            },
        ),
    ]
