# Generated by Django 4.1.7 on 2023-03-22 18:03

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
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=256, null=True, verbose_name='street address')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='City or neighborhood')),
                ('zipcode', models.CharField(blank=True, max_length=12, null=True, verbose_name='Zip / Postal code')),
                ('country', models.CharField(blank=True, max_length=64, null=True, verbose_name='Country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'db_table': 'addresses',
                'ordering': ['-user__date_joined'],
            },
        ),
    ]
