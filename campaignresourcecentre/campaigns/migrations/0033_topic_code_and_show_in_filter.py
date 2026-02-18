# Generated manually for CV-1396: Add code and show_in_filter fields to Topic model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "campaigns",
            "0032_alter_campaignhubpage_body_alter_campaignpage_body_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="code",
            field=models.CharField(max_length=50, unique=True, default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="topic",
            name="show_in_filter",
            field=models.BooleanField(
                default=True,
                help_text="Show this topic as a filter option on the campaigns page.",
            ),
        ),
    ]
