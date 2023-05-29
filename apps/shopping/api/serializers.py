from rest_framework import serializers

from apps.shopping.models import Cart, Order
from apps.users.api.serializers import UserSerializer


class OerderSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    productPubliId = serializers.CharField(source="product.public_id", read_only=True)
    orderDate = serializers.DateTimeField(source="order_date")
    user = UserSerializer()

    class Meta:
        model = Order
        fields = ["publicId", "productPubliId", "quantity", "ordered", "orderDate", "user"]


class CartSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    orders = OerderSerializer(many=True, read_only=True)
    orderStatus = serializers.CharField(source="order_status", read_only=True)
    paymentStatus = serializers.CharField(source="payment_status", read_only=True)
    orderDate = serializers.DateTimeField(source="order_date", read_only=True)
    paymentDate = serializers.DateTimeField(source="payment_date", read_only=True)
    deliveryDate = serializers.DateTimeField(source="delivery_date", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "publicId",
            "user",
            "orders",
            "orderStatus",
            "paymentStatus",
            "orderDate",
            "paymentDate",
            "deliveryDate",
        ]
