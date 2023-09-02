from rest_framework import serializers

from apps.payments.models import Payment
from apps.users.api.serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    user = UserSerializer(read_only=True)
    paymentStatus = serializers.FloatField(source="payment_status", read_only=True)
    orderStatus = serializers.CharField(source="order_status", read_only=True)
    paymentDate = serializers.DateTimeField(source="payment_date", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "publicId",
            "user",
            "ordersItems",
            "orderStatus",
            "totalPrice",
            "orderDate",
            "deliveryDate",
        ]
