# Generated by Django 5.0.1 on 2024-01-18 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
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
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books_app.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
