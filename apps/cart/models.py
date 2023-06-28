from typing import Any, Dict, Tuple

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.products.models import Product
from apps.users.models import User


class OrderItem(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(
        _("quantity"), default=1, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    ordered = models.BooleanField(_("ordered"), default=False, db_index=True)

    class Meta(AbstractCreatedUpdatedMixin.Meta):
        db_table = "order_item"
        verbose_name = _("Order Item")
        verbose_name_plural = _("  Orders Items")

    @property
    def total_price(self) -> float:
        return self.price * self.quantity

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        self.price = self.product.price_discount * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity}) <{self.user.name}>"


class Cart(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    orders_items = models.ManyToManyField(OrderItem, related_name="cart", blank=True)
    total_price = models.DecimalField(
        _("total price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )

    class Meta:
        db_table = "cart"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ["-updated_at"]

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        # self.total_price = self.orders_items.aggregate(models.Sum("price"))["price__sum"]
        return super().save(*args, **kwargs)

    def delete(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        self.orders_items.all().delete()
        return super().delete(*args, **kwargs)

    def clear(self) -> None:
        """
        Clear all items from the orders_items queryset and return None.
        """
        self.orders_items.all().delete()
        return None

    def __str__(self) -> str:
        return f"{self.user.name}"
