# Generated by Django 4.1.7 on 2023-03-16 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('ordered', models.BooleanField(db_index=True, default=False, verbose_name='status ordered')),
                ('order_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='order date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '  Order item',
                'verbose_name_plural': '  Order items',
                'db_table': 'order_items',
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('total_prices', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total prices')),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('delivered', 'Delivered'), ('returned', 'Returned'), ('cancelled', 'Cancelled')], db_index=True, default='pending', max_length=20, verbose_name='status')),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('awaiting_payment', 'Awaiting payment'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='payment status')),
                ('order_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='order date')),
                ('payment_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='payment date')),
                ('delivery_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='delivery date')),
                ('order_items', models.ManyToManyField(related_name='orders', to='shopping.orderitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ' Order',
                'verbose_name_plural': ' Orders',
                'db_table': 'orders',
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
            ],
            options={
                'verbose_name': 'Order history',
                'verbose_name_plural': 'Order history',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('shopping.order',),
        ),
    ]
