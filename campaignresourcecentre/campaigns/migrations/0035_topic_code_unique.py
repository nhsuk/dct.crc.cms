# Generated manually for CV-1396: Make Topic.code unique and non-null

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0034_populate_topics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="code",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
