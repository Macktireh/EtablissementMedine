from django.contrib import admin

from apps.cart.admin import CartAdmin as CartAdminBase, OrderItemAdmin as OrderItemAdminBase
from apps.orders.models import CartProxy, Order, OrderItemProxy, PaymentProxy
from apps.payments.admin import PaymentAdmin as PaymentAdminBase


@admin.register(CartProxy)
class CartAdmin(CartAdminBase):
    pass


@admin.register(PaymentProxy)
class PaymentProxyAdmin(PaymentAdminBase):
    pass


@admin.register(OrderItemProxy)
class OrderItemAdmin(OrderItemAdminBase):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "_orders_items",
        "total_price",
        "order_status",
        "payement",
        "order_date",
        "delivery_date",
    )
    list_filter = (
        "order_status",
        "order_date",
    )
    readonly_fields = ("total_price",)

    def _orders_items(self, obj: Order) -> str:
        return obj.orders_items.count()
