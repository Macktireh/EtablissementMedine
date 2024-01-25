from typing import Any, Dict, Tuple

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.core.models import IndexedTimeStampedModel, PublicIdModel
from apps.products.models import Product
from apps.users.models import User


class OrderItem(PublicIdModel, IndexedTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(
        _("quantity"), default=1, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    total_price = models.DecimalField(
        _("total price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    ordered = models.BooleanField(_("ordered"), default=False, db_index=True)

    class Meta(IndexedTimeStampedModel.Meta):
        db_table = "order_item"
        verbose_name = _("Order Item")
        verbose_name_plural = _("Orders Items")

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        if self.ordered is False:
            self.total_price = self.quantity * self.product.price
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity}) <{self.user.name}>"


class Cart(PublicIdModel, IndexedTimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    orders_items = models.ManyToManyField(OrderItem, related_name="cart", blank=True)

    @property
    def total_price(self) -> float:
        return self.orders_items.aggregate(Sum("total_price"))["total_price__sum"]

    class Meta:
        db_table = "cart"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ["-updated_at"]

    def delete(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        self.orders_items.all().delete()
        return super().delete(*args, **kwargs)

    def clear(self) -> None:
        """
        Clear all items from the orders_items queryset and return None.
        """
        self.orders_items.all().delete()
        return self.save()

    def __str__(self) -> str:
        return f"{self.user.name}"
