from rest_framework import serializers

from apps.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    publicId = serializers.CharField(source='public_id', read_only=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    phoneNnumber = serializers.CharField(source='phone_number')

    class Meta:
        model = User
        fields = ['publicId', 'firstName', 'lastName', 'phoneNnumber']
