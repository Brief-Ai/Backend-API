# Generated by Django 4.2.3 on 2023-07-31 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("author", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("url", models.CharField(max_length=255)),
                ("source", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("category", models.CharField(max_length=255)),
                ("language", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("published_at", models.CharField(max_length=255)),
            ],
            options={"verbose_name_plural": "articles",},
        ),
        migrations.CreateModel(
            name="Search",
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
                ("query", models.CharField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
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
