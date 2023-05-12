from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    phoneNnumber = serializers.CharField(source="phone_number")

    class Meta:
        model = User
        fields = ["publicId", "name", "email", "phoneNnumber"]
