from rest_framework import serializers

from apps.cart.models import Cart, OrderItem
from apps.users.api.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    user = UserSerializer(read_only=True)
    productPubliId = serializers.CharField(source="product.public_id", read_only=True)
    totalPrice = serializers.FloatField(source="total_price", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["publicId", "user", "productPubliId", "quantity", "ordered", "totalPrice"]


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ordersItems = OrderItemSerializer(source="orders_items", many=True, read_only=True)
    totalPrice = serializers.FloatField(source="total_price", read_only=True)

    class Meta:
        model = Cart
        fields = ["user", "ordersItems", "totalPrice"]


class AddToCartSerializer(serializers.Serializer):
    productPublicId = serializers.CharField(write_only=True)


class UpdateOrderItemQuantitySerializer(serializers.Serializer):
    orderItemPublicId = serializers.CharField(write_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=100, write_only=True)
