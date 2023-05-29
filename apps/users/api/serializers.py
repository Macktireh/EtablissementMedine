from rest_framework import serializers

from apps.users.models import Address, User


class UserSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    phoneNnumber = serializers.CharField(source="phone_number")

    class Meta:
        model = User
        fields = ["publicId", "name", "email", "phoneNnumber"]
        read_only_fields = ["email"]


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    streetAddress = serializers.CharField(source="street_address")

    class Meta:
        model = Address
        exclude = ["id", "street_address"]
