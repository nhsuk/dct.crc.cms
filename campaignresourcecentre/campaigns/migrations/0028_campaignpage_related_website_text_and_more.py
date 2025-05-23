# Generated by Django 4.0.4 on 2022-06-17 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("campaigns", "0027_alter_campaignpage_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaignpage",
            name="related_website_text",
            field=models.CharField(
                blank=True,
                help_text="Enter the text for the link. This is required for external URLs. If an internal page is chosen and this field is blank the page title will be shown",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="campaignpage",
            name="related_website",
            field=models.URLField(blank=True, help_text="Enter a URL to link to."),
        ),
    ]
