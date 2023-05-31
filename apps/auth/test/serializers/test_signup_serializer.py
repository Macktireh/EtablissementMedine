from typing import Any

import pytest
from django.contrib.auth import get_user_model

from apps.auth.api.serializers import SignupSerializer

User = get_user_model()


@pytest.mark.django_db
class TestSignupSerializer:
    @classmethod
    def setup_class(cls) -> None:
        cls.user_attributes = {
            "name": "Bob Smith",
            "email": "bob.smith@example.com",
            "phoneNumber": "77001234",
            "password": "Password@123",
        }
        cls.payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phoneNumber": "77123456",
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }

    @pytest.fixture
    def create_user(self) -> User:
        user_attributes = self.user_attributes.copy()
        phone_number = user_attributes["phoneNumber"]
        del user_attributes["phoneNumber"]
        user_attributes["phone_number"] = phone_number
        user = User.objects.create_user(**user_attributes)
        return user

    def test_login_serializer_is_valid(self, client: Any, create_user: User) -> None:
        serializer = SignupSerializer(data=self.payload)
        assert serializer.is_valid() is True
        assert serializer.data["email"] == self.payload["email"]
        assert serializer.data["name"] == self.payload["name"]
        assert serializer.data["phoneNumber"] == self.payload["phoneNumber"]
        with pytest.raises(KeyError):
            serializer.data["password"]
        with pytest.raises(KeyError):
            serializer.data["confirmPassword"]

    def test_login_serializer_is_not_valid(self, client: Any, create_user: User) -> None:
        # email already exists
        payload = self.user_attributes.copy()
        payload["phoneNumber"] = "77000012"
        payload["confirmPassword"] = payload["password"]
        serializer = SignupSerializer(data=payload)
        assert serializer.is_valid() is False

        # phone number already exists
        payload = self.user_attributes.copy()
        payload["email"] = "test@example.com"
        payload["confirmPassword"] = payload["password"]
        serializer = SignupSerializer(data=payload)
        assert serializer.is_valid() is False

        # password is too short or weak
        payload = self.payload.copy()
        payload["password"] = "12345"
        payload["confirmPassword"] = "12345"
        serializer = SignupSerializer(data=payload)
        assert serializer.is_valid() is False

        # without confirm password
        payload = self.payload.copy()
        del payload["confirmPassword"]
        serializer = SignupSerializer(data=payload)
        assert serializer.is_valid() is False

        # password and confirm password do not match
        payload = self.payload.copy()
        payload["confirmPassword"] = "Password@"
        serializer = SignupSerializer(data=payload)
        assert serializer.is_valid() is False
