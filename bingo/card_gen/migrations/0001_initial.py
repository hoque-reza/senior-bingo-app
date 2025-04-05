# Generated by Django 4.2.19 on 2025-02-23 03:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BingoCard",
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
                (
                    "serial_number",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "player_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("expiry_date", models.DateField()),
                ("numbers", models.JSONField()),
                ("is_claimed", models.BooleanField(default=False)),
            ],
        ),
    ]
