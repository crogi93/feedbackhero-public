# Generated by Django 4.1.4 on 2024-01-22 10:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_remove_comment_author_email_remove_comment_author_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="body",
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="suggestion",
            name="description",
            field=models.TextField(max_length=1000),
        ),
    ]
