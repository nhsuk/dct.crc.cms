# Generated by Django 2.0.9 on 2018-10-02 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("documents", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="customdocument",
            name="file_size",
            field=models.PositiveIntegerField(editable=False, null=True),
        )
    ]
