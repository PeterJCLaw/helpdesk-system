# Generated by Django 3.2.17 on 2023-02-06 17:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
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
                    "tla",
                    models.CharField(
                        max_length=4,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Z]{3}\\d*$", "Must match TLA format."
                            )
                        ],
                        verbose_name="TLA",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Team Name")),
                ("is_rookie", models.BooleanField(verbose_name="Is Rookie")),
            ],
        ),
    ]
