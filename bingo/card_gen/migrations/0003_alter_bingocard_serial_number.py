# Generated by Django 4.2.19 on 2025-03-10 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("card_gen", "0002_callednumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bingocard",
            name="serial_number",
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]
