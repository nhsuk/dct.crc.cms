# Generated by Django 3.1.13 on 2021-10-14 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0002_customimage_file_hash"),
        ("home", "0015_auto_20210914_1333"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="hero_align",
            field=models.CharField(
                choices=[("left", "Left"), ("center", "Center"), ("right", "Right")],
                default="right",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_image",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
    ]
