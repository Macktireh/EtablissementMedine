from rest_framework import serializers

from apps.cart.api.serializers import OrderItemSerializer
from apps.orders.models import Order
from apps.users.api.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    user = UserSerializer(read_only=True)
    ordersItems = OrderItemSerializer(many=True, read_only=True)
    totalPrice = serializers.FloatField(source="total_price", read_only=True)
    orderStatus = serializers.CharField(source="order_status", read_only=True)
    orderDate = serializers.DateTimeField(source="order_date", read_only=True)
    deliveryDate = serializers.DateTimeField(source="delivery_date", read_only=True)

    class Meta:
        model = Order
        fields = [
            "publicId",
            "user",
            "ordersItems",
            "orderStatus",
            "totalPrice",
            "orderDate",
            "deliveryDate",
        ]
