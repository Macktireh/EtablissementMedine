from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.product.models import Product
from apps.base.models import AbstractPublicIdMixin, AbstractCreatedUpdatedMixin


User = get_user_model()


class OrderItem(AbstractPublicIdMixin):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    is_ordered = models.BooleanField(_('status ordered'), default=False)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = _('  Order item')
        verbose_name_plural = _('  Order items')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"


class Order(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_items = models.ManyToManyField(OrderItem, related_name='orders')
    total_prices = models.DecimalField(_('total prices'), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_('status'), max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _(' Order')
        verbose_name_plural = _(' Orders')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.user.full_name}"


class OrderHistory(Order):
    
    class Meta:
        proxy = True
        verbose_name = _('Order history')
        verbose_name_plural = _('Order history')
