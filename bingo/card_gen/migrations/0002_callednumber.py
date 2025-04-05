# Generated by Django 4.2.19 on 2025-03-03 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("card_gen", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalledNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                ("called_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
