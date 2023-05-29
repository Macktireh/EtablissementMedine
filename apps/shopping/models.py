from typing import Any, Dict, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.product.models import Product
from apps.users.models import User


class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    PROCESSING = "processing", _("Processing")
    DELIVERED = "delivered", _("Delivered")
    RETURNED = "returned", _("Returned")
    CANCELLED = "cancelled", _("Cancelled")


class PaymentStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    COMPLETED = "completed", _("Completed")
    AWAITING_PAYMENT = "awaiting_payment", _("Awaiting payment")
    REFUNDED = "refunded", _("Refunded")
    CANCELLED = "cancelled", _("Cancelled")


class Order(AbstractPublicIdMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0.00)
    ordered = models.BooleanField(_("ordered"), default=False, db_index=True)
    order_date = models.DateTimeField(_("order date"), blank=True, null=True, db_index=True)

    class Meta:
        db_table = "order"
        verbose_name = _("Order")
        verbose_name_plural = _("  Orders")
        ordering = ["-order_date"]

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity}) <{self.user.name}>"

    def save(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        self.price = self.product.price_discount * self.quantity
        return super().save(*args, **kwargs)


class Cart(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    orders = models.ManyToManyField(Order, related_name="orders")
    order_status = models.CharField(
        _("order status"),
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
        db_index=True,
    )
    payment_status = models.CharField(
        _("payment status"),
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
    order_date = models.DateTimeField(_("order date"), blank=True, null=True, db_index=True)
    payment_date = models.DateTimeField(_("payment date"), blank=True, null=True, db_index=True)
    delivery_date = models.DateTimeField(_("delivery date"), blank=True, null=True, db_index=True)

    class Meta:
        db_table = "cart"
        verbose_name = _("Cart")
        verbose_name_plural = _(" Carts")
        ordering = ["-order_date"]

    def __str__(self) -> str:
        return f"{self.user.name}"

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        self.orders.all().delete()
        return super().delete(*args, **kwargs)


class CartHistory(Cart):
    class Meta:
        proxy = True
        verbose_name = _("Cart history")
        verbose_name_plural = _("Cart history")

    def __str__(self) -> str:
        return f"{self.user.name}"
