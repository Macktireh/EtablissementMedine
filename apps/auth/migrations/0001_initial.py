# Generated by Django 4.2.1 on 2023-06-28 14:34

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupProxy",
            fields=[],
            options={
                "verbose_name": "group",
                "verbose_name_plural": "groups",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.group",),
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserProxy",
            fields=[],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.user",),
        ),
        migrations.CreateModel(
            name="CodeChecker",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("token", models.CharField(max_length=6)),
                ("verified", models.BooleanField(db_index=True, default=False, verbose_name="verified")),
                (
                    "timestamp_requested",
                    models.DateTimeField(auto_now_add=True, verbose_name="timestamp requested"),
                ),
                ("timestamp_verified", models.DateTimeField(null=True, verbose_name="timestamp verified")),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "verbose_name": "code checker",
                "verbose_name_plural": "code checkers",
                "db_table": "code_checker",
            },
        ),
    ]
