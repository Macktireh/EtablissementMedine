from typing import Any

import pytest
from django.contrib.auth import get_user_model

from apps.auth.api.serializers import ResetPasswordSerializer

User = get_user_model()


@pytest.mark.django_db
class TestResetPasswordSerializer:
    @classmethod
    def setup_class(cls) -> None:
        cls.payload = {
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }

    @pytest.fixture
    def _serializer(self) -> ResetPasswordSerializer:
        serializer = ResetPasswordSerializer(data=self.payload)
        return serializer

    def test_reset_password_serializer_is_valid(
        self, client: Any, _serializer: ResetPasswordSerializer
    ) -> None:
        assert _serializer.is_valid()
        with pytest.raises(KeyError):
            _serializer.data["password"]
        with pytest.raises(KeyError):
            _serializer.data["confirmPassword"]

    def test_reset_password_serializer_is_not_valid(
        self, client: Any, _serializer: ResetPasswordSerializer
    ) -> None:
        serializer1 = ResetPasswordSerializer(data={"password": "Password@123"})
        assert serializer1.is_valid() is False
        serializer2 = ResetPasswordSerializer(
            data={"password": "Password@123", "confirmPassword": "Password@"}
        )
        assert serializer2.is_valid() is False
