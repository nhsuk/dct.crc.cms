# Generated by Django 4.0.4 on 2022-08-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("campaigns", "0029_campaignpage_campaign_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignpage",
            name="campaign_end_date",
            field=models.TextField(
                blank=True,
                help_text="Use the date format: 3 September 2022. If the campaign has always on assets, put: Always on",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="campaignpage",
            name="campaign_start_date",
            field=models.TextField(blank=True, max_length=25),
        ),
    ]
