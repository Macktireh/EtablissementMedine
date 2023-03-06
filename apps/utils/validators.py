import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.utils.response import failMsg


User = get_user_model()


def phoneNumverValidator(value: str) -> str:
    if not re.match(r'^77\d{6}$', value):
        raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_DJIBOUTIAN_TELEPHONE_NUMBER"])
    if User.objects.filter(phone_number__iexact=value).exists():
        raise serializers.ValidationError(failMsg["THE_TELEPHONE_NUMBER_ALREADY_EXISTS"])
    return value


def emailValidator(value: str) -> str:
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", value):
        raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_EMAIL_ADDRESS"])
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError(failMsg["THE_EMAIL_ADDRESS_ALREADY_EXISTS"])
    return value


def passwordValidator(value: str) -> str:
    if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", value):
        raise serializers.ValidationError(failMsg["INVALID_PASSWORD"])
    return value
