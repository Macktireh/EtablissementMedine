# Generated by Django 4.2.1 on 2023-06-28 14:35

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
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("public_id", models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="updated at")),
                (
                    "type",
                    models.CharField(
                        choices=[("cash", "Cash"), ("credit_card", "Credit card")],
                        default="cash",
                        max_length=20,
                        verbose_name="payment type",
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("awaiting", "Awaiting"),
                            ("successful", "Successful"),
                            ("failed", "Failed"),
                        ],
                        db_index=True,
                        default="awaiting",
                        max_length=20,
                        verbose_name="payment status",
                    ),
                ),
                (
                    "payment_date",
                    models.DateTimeField(blank=True, db_index=True, null=True, verbose_name="payment date"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
                "db_table": "payment",
            },
        ),
    ]
