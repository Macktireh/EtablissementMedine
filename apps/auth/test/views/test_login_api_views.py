from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.users.types import UserType

User = get_user_model()


@pytest.mark.django_db
class TestLoginApiView:
    @classmethod
    def setup_class(cls) -> None:
        cls.valid_data_1 = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "77123456",
            "password": "Password@123",
        }
        cls.valid_data_2 = {
            "name": "John Doe",
            "email": "john-doe@example.com",
            "phone_number": "77123457",
            "password": "Password@123",
        }

        cls.url = reverse("authApi:login-api")

    @pytest.fixture
    def create_user(self) -> tuple[User, User]:
        user1: UserType = User.objects.create_user(**self.valid_data_1)
        user1.verified = True
        user1.save()
        user2: UserType = User.objects.create_user(**self.valid_data_2)
        return user1, user2

    def test_login_success(self, client: Any, create_user) -> None:
        payload = self.valid_data_1.copy()
        del payload["name"]
        del payload["phone_number"]
        response = client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_login_fail_with_user_not_verified(self, client: Any, create_user) -> None:
        payload = self.valid_data_2.copy()
        del payload["name"]
        del payload["phone_number"]
        response = client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_login_fail_with_invalid_credentials(self, client: Any, create_user) -> None:
        payload = {"email": "test@example.com", "password": "password"}
        response = client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
