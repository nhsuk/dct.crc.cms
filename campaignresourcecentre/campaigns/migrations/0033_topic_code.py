# Generated manually for CV-1396: Add code field to Topic model

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
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
