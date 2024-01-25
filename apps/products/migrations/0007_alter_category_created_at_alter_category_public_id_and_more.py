# Generated by Django 4.2.4 on 2023-12-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_alter_product_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="category",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="groupcategory",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="groupcategory",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="groupcategory",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="product",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="productadvertising",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="productadvertising",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="productadvertising",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="public_id",
            field=models.CharField(
                db_index=True,
                editable=False,
                help_text="Unique identifier for this object. This is used to identify ",
                max_length=64,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name="updated at"),
        ),
    ]
