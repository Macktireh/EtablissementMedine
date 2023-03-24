from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.shopping.models import Cart, CartHistory, Order, OrderStatusChoices


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('product', 'quantity', 'price', 'ordered', 'order_date',)
    list_filter = ('ordered', 'order_date',)
    readonly_fields = ('price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ('customer_name', '_orders', 'order_status', 'payment_status', 'payment_date', 'delivery_date',)
    list_filter = ('order_status', 'payment_status', 'order_date',)

    def customer_name(self, obj: Cart) -> str:
        return obj.user.get_full_name()
    
    def _orders(self, obj: Cart) -> str:
        return obj.orders.count()
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user').filter(order_status=OrderStatusChoices.PENDING)


@admin.register(CartHistory)
class CartHistoryAdmin(admin.ModelAdmin):

    list_display = ('customer_name', '_orders', 'order_status', 'payment_status', 'order_date', 'payment_date', 'delivery_date',)
    list_filter = ('order_status', 'payment_status', 'order_date', 'payment_date', 'delivery_date')

    def customer_name(self, obj: CartHistory) -> str:
        return obj.user.get_full_name()
    
    def _orders(self, obj: CartHistory) -> str:
        return obj.orders.count()

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: CartHistory = None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: CartHistory = None) -> bool:
        return False
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).exclude(order_status=OrderStatusChoices.PENDING)
