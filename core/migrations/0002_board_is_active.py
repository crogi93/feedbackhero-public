# Generated by Django 4.1.4 on 2024-02-14 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
