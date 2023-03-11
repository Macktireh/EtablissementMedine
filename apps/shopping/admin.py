from django.contrib import admin

from apps.shopping.models import Order, OrderHistory, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'is_ordered', 'order_date',)
    list_filter = ('is_ordered', 'order_date',)


@admin.register(Order)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer_name', '_orders', 'status', 'order_date',)
    list_filter = ('status', 'order_date',)

    def customer_name(self, obj) -> str:
        return obj.user.full_name
    
    def _orders(self, obj) -> str:
        return obj.orders.count()


@admin.register(OrderHistory)
class CartHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', '_orders', 'status', 'order_date',)
    list_filter = ('status', 'order_date',)

    def customer_name(self, obj) -> str:
        return obj.user.full_name
    
    def _orders(self, obj) -> str:
        return obj.orders.count()

    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False