from rest_framework import serializers

from apps.customer.serializers import UserSerializer
from apps.shopping.models import Cart, Order


class OerderSerializer(serializers.ModelSerializer):

    publicId = serializers.CharField(source='public_id', read_only=True)
    user = UserSerializer()
    productPubliId = serializers.CharField(source='product.public_id', read_only=True)
    quantity = serializers.IntegerField(source='quantity', read_only=True)
    ordered = serializers.BooleanField(source='ordered', read_only=True)
    orderDate = serializers.DateTimeField(source='order_date', read_only=True)

    class Meta:
        model = Order
        fields = ['publicId', 'user', 'productPubliId', 'quantity', 'ordered', 'orderDate']


class CartSerializer(serializers.ModelSerializer):

    publicId = serializers.CharField(source='public_id', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    orders = OerderSerializer(many=True, read_only=True)
    orderStatus = serializers.CharField(source='order_status', read_only=True)
    paymentStatus = serializers.CharField(source='payment_status', read_only=True)
    orderDate = serializers.DateTimeField(source='order_date', read_only=True)
    paymentDate = serializers.DateTimeField(source='payment_date', read_only=True)
    deliveryDate = serializers.DateTimeField(source='delivery_date', read_only=True)

    class Meta:
        model = Cart
        fields = ['publicId', 'user', 'orders', 'orderStatus', 'paymentStatus', 'orderDate', 'paymentDate', 'deliveryDate']
        
