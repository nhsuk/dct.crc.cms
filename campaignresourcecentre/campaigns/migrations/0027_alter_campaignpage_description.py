# Generated by Django 4.0.3 on 2022-04-01 14:44

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("campaigns", "0026_alter_campaignupdate_link_page"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignpage",
            name="description",
            field=wagtail.fields.RichTextField(
                help_text="Introduction section for the campaign page. This is limited to 480 characters to make sure the page loads properly on frontend. Please preview the page before you publish as this depends on length of the below image and may alter the page overall design."
            ),
        ),
    ]
