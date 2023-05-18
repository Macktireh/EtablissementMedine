import pytest
from typing import Any

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status


User = get_user_model()


@pytest.mark.django_db
class TestSignupApiView:

    @classmethod
    def setup_class(cls) -> None:
        cls.valid_data = {
            "name": "John Doe",
            "email": "test@example.com",
            "phoneNumber": "77123456",
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }
        cls.url = reverse("authApi:signup-api")
    
    @pytest.fixture
    def create_user(self) -> User:
        data = self.valid_data.copy()
        phone_number = data["phoneNumber"]
        del data["phoneNumber"]
        del data["confirmPassword"]
        data["phone_number"] = phone_number
        return User.objects.create_user(**data)

    def test_signup_success(self, client: Any) -> None:
        response = client.post(self.url, data=self.valid_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_signup_fail_with_empty_data(self, client: Any) -> None:
        response = client.post(self.url, data={}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signup_fail_with_user_already_exists(self, client: Any, create_user: User) -> None:
        response = client.post(self.url, data=self.valid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
