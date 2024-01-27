# Generated by Django 4.2.1 on 2023-06-28 14:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",  # noqa: E501
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined"),
                ),
                ("public_id", models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ("name", models.CharField(max_length=128, verbose_name="name")),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=255, unique=True, verbose_name="email address"),
                ),
                (
                    "phone_number",
                    models.CharField(db_index=True, max_length=24, unique=True, verbose_name="phone number"),
                ),
                (
                    "verified",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this user has been verified.",
                        verbose_name="verified",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",  # noqa: E501
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "user",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                (
                    "street_address",
                    models.CharField(blank=True, max_length=256, null=True, verbose_name="street address"),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=128, null=True, verbose_name="City or neighborhood"),
                ),
                (
                    "zipcode",
                    models.CharField(blank=True, max_length=12, null=True, verbose_name="Zip / Postal code"),
                ),
                ("country", models.CharField(blank=True, max_length=64, null=True, verbose_name="Country")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
                "db_table": "address",
                "ordering": ["-user__date_joined"],
            },
        ),
    ]
