# Generated by Django 4.2.1 on 2023-08-10 11:15

import apps.products.utils
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="thumbnail",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="JPEG",
                keep_meta=True,
                null=True,
                quality=90,
                scale=None,
                size=[500, 500],
                upload_to=apps.products.utils.thumbnail_path_product,
                verbose_name="thumbnail",
            ),
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
                size=[500, 500],
                upload_to=apps.products.utils.thumbnail_path_product,
                verbose_name="thumbnail",
            ),
        ),
    ]
