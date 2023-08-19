from django.contrib import admin
from django.db.models import Sum
from django.http import HttpRequest

from apps.cart.models import Cart


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "total_price",
        "ordered",
    )
    list_filter = ("ordered",)
    readonly_fields = ("total_price",)


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "_orders_items",
        "total_price",
    )
    readonly_fields = ("total_price",)

    def _orders_items(self, obj: Cart) -> int:
        return obj.orders_items.aggregate(Sum("quantity"))["quantity__sum"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Cart = None) -> bool:
        return request.user.is_superuser

    def has_change_permission(self, request: HttpRequest, obj: Cart = None) -> bool:
        # return False
        return request.user.is_superuser
