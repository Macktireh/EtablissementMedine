from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.product.models import Product

from apps.base.models import AbstractPublicIdMixin, AbstractCreatedUpdatedMixin


User = get_user_model()


class OrderItem(AbstractPublicIdMixin):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    is_ordered = models.BooleanField(_('status ordered'), default=False)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"


class Cart(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    order_items = models.ManyToManyField(OrderItem, related_name='carts')
    total_price = models
    status = models.CharField(_('status'), max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    order_date = models.DateTimeField(_('order date'), blank=True, null=True)

    class Meta:
        db_table = 'carts'
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')
        ordering = ['-order_date']

    def __str__(self) -> str:
        return f"{self.user.full_name}"


class CartHistory(Cart):
    
    class Meta:
        proxy = True
        verbose_name = _('Cart history')
        verbose_name_plural = _('Cart history')
