from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.auth.utils import make_token

User = get_user_model()


class TestRequestActivationAPIView(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.client = APIClient()
        self.url = reverse("authApi:request-activation-api")

    def test_request_activation_success(self) -> None:
        payload = {"email": "test@example.com"}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activation_invalid_data(self) -> None:
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestActivationAPIView(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.client = APIClient()
        self.user_data = {
            "name": "Test User",
            "phoneNumber": "77123456",
            "email": "test@example.com",
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }
        self.url = reverse("authApi:activation-api")

    def signup(self) -> User:
        self.client.post(reverse("authApi:signup-api"), data=self.user_data, format="json")
        return User.objects.get(email=self.user_data["email"])

    def expired(self, user: User) -> str:
        from apps.auth.models import CodeChecker

        obj = CodeChecker.objects.get(user=user)
        obj.timestamp_requested = timezone.now() - timedelta(minutes=4)
        obj.save()
        return None

    def test_activation_success(self) -> None:
        user = self.signup()
        payload = {"email": self.user_data["email"], "token": make_token(user)}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activation_invalid_data(self) -> None:
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activation_token_expired(self) -> None:
        user = self.signup()
        self.expired(user)
        payload = {"email": self.user_data["email"], "token": make_token(user)}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
