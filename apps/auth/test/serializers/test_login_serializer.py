from typing import Any

import pytest
from django.contrib.auth import get_user_model

from apps.auth.api.serializers import LoginSerializer

User = get_user_model()


@pytest.mark.django_db
class TestLoginSerializer:
    @classmethod
    def setup_class(cls) -> None:
        cls.payload = {
            "email": "test@example.com",
            "password": "Password@123",
        }

    @pytest.fixture
    def serializer(self) -> LoginSerializer:
        serializer = LoginSerializer(data=self.payload)
        return serializer

    def test_login_serializer_is_valid(self, client: Any, serializer: LoginSerializer) -> None:
        assert serializer.is_valid()
        assert serializer.data["email"] == self.payload["email"]
        with pytest.raises(KeyError):
            serializer.data["password"]

    def test_login_serializer_is_not_valid(self, client: Any, serializer: LoginSerializer) -> None:
        serializer = LoginSerializer(data={"email": "test@example.com"})
        assert not serializer.is_valid()
        serializer = LoginSerializer(data={"password": "Password@123"})
        assert not serializer.is_valid()
        serializer = LoginSerializer(data={"password": "Password@123"})
        assert not serializer.is_valid()
