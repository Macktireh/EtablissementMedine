# Generated by Django 4.2.1 on 2023-08-19 19:01

import colorfield.fields
import django_resized.forms
from django.db import migrations, models

import apps.products.utils


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_product_color_product_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                (
                    "name",
                    colorfield.fields.ColorField(
                        blank=True,
                        default=None,
                        image_field=None,
                        max_length=18,
                        null=True,
                        samples=None,
                        verbose_name="color",
                    ),
                ),
            ],
            options={
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
                "db_table": "color",
            },
        ),
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
        migrations.RemoveField(
            model_name="product",
            name="color",
        ),
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="JPEG",
                keep_meta=True,
                null=True,
                quality=90,
                scale=None,
                size=[700, 700],
                upload_to=apps.products.utils.thumbnail_path_product,
                verbose_name="thumbnail",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.ManyToManyField(related_name="products", to="products.color"),
        ),
    ]
