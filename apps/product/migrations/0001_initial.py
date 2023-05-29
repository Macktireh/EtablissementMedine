# Generated by Django 4.2.1 on 2023-05-28 19:30

import apps.product.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="name")),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True, verbose_name="name"
                    ),
                ),
                (
                    "name_fr",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True, verbose_name="name"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "thumbnail",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="PNG",
                        keep_meta=True,
                        null=True,
                        quality=90,
                        scale=None,
                        size=[200, 200],
                        upload_to=apps.product.utils.thumbnail_path,
                        verbose_name="thumbnail",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "db_table": "category",
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="name")),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True, verbose_name="name"
                    ),
                ),
                (
                    "name_fr",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True, verbose_name="name"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True, verbose_name="slug")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="stock quantity")),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name="price"),
                ),
                (
                    "discount",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="discount",
                    ),
                ),
                (
                    "price_discount",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="price discount"),
                ),
                (
                    "expiry_date_discount",
                    models.DateTimeField(blank=True, null=True, verbose_name="expiry date discount"),
                ),
                ("description", models.TextField(blank=True, null=True, verbose_name="description")),
                ("description_en", models.TextField(blank=True, null=True, verbose_name="description")),
                ("description_fr", models.TextField(blank=True, null=True, verbose_name="description")),
                (
                    "thumbnail",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="JPEG",
                        keep_meta=True,
                        null=True,
                        quality=90,
                        scale=None,
                        size=[400, 400],
                        upload_to=apps.product.utils.thumbnail_path,
                        verbose_name="thumbnail",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "product",
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
    ]
