from collections import OrderedDict

from rest_framework import serializers

from apps.auth.models import User
from apps.auth.validators import AuthUserValidators
from apps.core.response import failMsg


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128,
        validators=[AuthUserValidators.passwordValidator],
        write_only=True,
        style={"input_type": "password"},
    )
    confirmPassword = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})


class SignupSerializer(PasswordSerializer):
    name = serializers.CharField(max_length=128)
    phoneNumber = serializers.CharField(
        source="phone_number",
        max_length=24,
        validators=[AuthUserValidators.phoneNumberValidator],
    )
    email = serializers.CharField(validators=[AuthUserValidators.emailValidator])

    class Meta:
        fields = [
            "name",
            "phoneNumber",
            "email",
            "password",
            "confirmPassword",
        ]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get("password")
        confirm_password = attrs.get("confirmPassword")
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(
                {"confirmPassword": failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"]}
            )
        return attrs

    def create(self, validate_data: dict) -> User:
        validate_data.pop("confirmPassword", None)
        return User.objects.create_user(**validate_data)


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})


class RequestActivationOrResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)


class ResetPasswordSerializer(PasswordSerializer):
    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get("password")
        confirm_password = attrs.get("confirmPassword")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(
                {"confirmPassword": failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"]}
            )
        return attrs
