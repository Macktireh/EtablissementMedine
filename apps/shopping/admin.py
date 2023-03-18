from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from apps.shopping.models import Order, OrderHistory, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('product', 'quantity', 'ordered', 'order_date',)
    list_filter = ('ordered', 'order_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('customer_name', '_orders', 'order_status', 'payment_status', 'payment_date', 'delivery_date',)
    list_filter = ('order_status', 'payment_status', 'order_date',)

    def customer_name(self, obj: Order) -> str:
        return obj.user.full_name
    
    def _orders(self, obj: Order) -> str:
        return obj.orders.count()
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user')


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):

    list_display = ('customer_name', '_orders', 'order_status', 'payment_status', 'payment_date', 'delivery_date',)
    list_filter = ('order_status', 'payment_status', 'order_date',)

    def customer_name(self, obj: OrderHistory) -> str:
        return obj.user.full_name
    
    def _orders(self, obj: OrderHistory) -> str:
        return obj.orders.count()

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: OrderHistory = None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: OrderHistory = None) -> bool:
        return False