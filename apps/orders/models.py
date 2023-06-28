from typing import Any, Dict, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.cart.models import Cart, OrderItem
from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.payments.models import Payment
from apps.users.models import User


class CartProxy(Cart):
    class Meta:
        proxy = True
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class PaymentProxy(Payment):
    class Meta:
        proxy = True
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")


class OrderItemProxy(OrderItem):
    class Meta:
        proxy = True
        verbose_name = _("Order Item")
        verbose_name_plural = _("Orders Items")


class OrderStatusChoices(models.TextChoices):
    IN_PROGRESS = "in_progress", _("In progress")
    COMPLETED = "completed", _("Completed")
    CANCELLED = "cancelled", _("Cancelled")
    REFUNDED = "refunded", _("Refunded")


class Order(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    orders_items = models.ManyToManyField(OrderItem, related_name="orders", blank=True)
    total_price = models.DecimalField(
        _("total price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    order_status = models.CharField(
        _("order status"),
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.IN_PROGRESS,
        db_index=True,
    )
    payement = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="order")
    order_date = models.DateTimeField(_("order date"), blank=True, null=True, db_index=True)
    delivery_date = models.DateTimeField(_("delivery date"), blank=True, null=True, db_index=True)

    class Meta:
        db_table = "order"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-order_date"]

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        # self.total_price = self.orders_items.aggregate(models.Sum("price"))["price__sum"]
        return super().save(*args, **kwargs)

    def delete(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        self.orders_items.all().delete()
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.name}"
