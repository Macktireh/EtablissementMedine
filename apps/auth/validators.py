import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.response import failMsg

User = get_user_model()


regexEmail = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"  # noqa: E501
regexPhoneNumber = r"^77\d{6}$"
regexPassword = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class AuthUserValidators:
    """Validators for the AuthUser class"""

    @staticmethod
    def phoneNumberValidator(value: str) -> str:
        """
        Validates a phone number and returns it if valid.

        Parameters:
            value (str): The phone number to be validated.

        Returns:
            str: The validated phone number.

        Raises:
            serializers.ValidationError: If the phone number is not valid or already exists.
        """
        if not re.match(regexPhoneNumber, value):
            raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_DJIBOUTIAN_TELEPHONE_NUMBER"])

        value = "+253" + value if not str(value).startswith("+253") else value

        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError(failMsg["THE_TELEPHONE_NUMBER_ALREADY_EXISTS"])

        return value

    @staticmethod
    def emailValidator(value: str) -> str:
        """
        Validates an email address and checks if it already exists in the database.

        Parameters:
            value (str): The email address to be validated.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If the email address is not valid or already exists.
        """
        if not re.match(regexEmail, value):
            raise serializers.ValidationError(failMsg["PLEASE_ENTER_A_VALID_EMAIL_ADDRESS"])

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(failMsg["THE_EMAIL_ADDRESS_ALREADY_EXISTS"])

        return value

    @staticmethod
    def passwordValidator(value: str) -> str:
        """
        Validates the password based on a regular expression.

        Args:
            value (str): The password string to be validated.

        Returns:
            str: The validated password string.

        Raises:
            serializers.ValidationError: If the password does not match the regular expression.
        """
        if not re.match(regexPassword, value):
            raise serializers.ValidationError(failMsg["INVALID_PASSWORD"])
        return value
