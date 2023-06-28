from django.contrib import admin
from django.http import HttpRequest

from apps.cart.models import Cart, OrderItem


# @admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "total_price",
        "ordered",
    )
    list_filter = ("ordered",)


# @admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "_orders_items",
    )

    def _orders_items(self, obj: Cart) -> int:
        return obj.orders_items.count()

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Cart = None) -> bool:
        return request.user.is_superuser

    def has_change_permission(self, request: HttpRequest, obj: Cart = None) -> bool:
        return request.user.is_superuser
