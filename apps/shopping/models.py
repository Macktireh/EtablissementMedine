from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.auth.models import User
from apps.base.models import AbstractPublicIdMixin, AbstractCreatedUpdatedMixin
from apps.product.models import Product


class OrderStatusChoices(models.TextChoices):

    PENDING = 'pending', _('Pending')
    PROCESSING = 'processing', _('Processing')
    DELIVERED = 'delivered', _('Delivered')
    RETURNED = 'returned', _('Returned')
    CANCELLED = 'cancelled', _('Cancelled')


class PaymentStatusChoices(models.TextChoices):

    PENDING = 'pending', _('Pending')
    COMPLETED = 'completed', _('Completed')
    AWAITING_PAYMENT = 'awaiting_payment', _('Awaiting payment')
    REFUNDED = 'refunded', _('Refunded')
    CANCELLED = 'cancelled', _('Cancelled')


class OrderItem(AbstractPublicIdMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    ordered = models.BooleanField(_('status ordered'), default=False, db_index=True)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = _('  Order item')
        verbose_name_plural = _('  Order items')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"


class Order(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_items = models.ManyToManyField(OrderItem, related_name='orders')
    total_prices = models.DecimalField(_('total prices'), max_digits=10, decimal_places=2, default=0)
    order_status = models.CharField(_('status'), max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING, db_index=True)
    payment_status = models.CharField(_('payment status'), max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True, db_index=True)
    payment_date = models.DateTimeField(_('payment date'), blank=True, null=True, db_index=True)
    delivery_date = models.DateTimeField(_('delivery date'), blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _(' Order')
        verbose_name_plural = _(' Orders')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.user.full_name()}"


class OrderHistory(Order):

    class Meta:
        proxy = True
        verbose_name = _('Order history')
        verbose_name_plural = _('Order history')
