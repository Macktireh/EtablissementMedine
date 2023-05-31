import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.response import failMsg

User = get_user_model()


regexEmail = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
regexPhoneNumber = r"^77\d{6}$"
regexPassword = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class AuthUserValidators:
    @staticmethod
    def phoneNumberValidator(value: str) -> str:
        if not re.match(regexPhoneNumber, value):
            raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_DJIBOUTIAN_TELEPHONE_NUMBER"])
        if not str(value).startswith("+253"):
            value = "+253" + value
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError(failMsg["THE_TELEPHONE_NUMBER_ALREADY_EXISTS"])
        return value

    @staticmethod
    def emailValidator(value: str) -> str:
        if not re.match(regexEmail, value):
            raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_EMAIL_ADDRESS"])
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(failMsg["THE_EMAIL_ADDRESS_ALREADY_EXISTS"])
        return value

    @staticmethod
    def passwordValidator(value: str) -> str:
        if not re.match(regexPassword, value):
            raise serializers.ValidationError(failMsg["INVALID_PASSWORD"])
        return value
