from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestLoginAPIView(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.client = APIClient()
        self.user_data = {
            "name": "Test User",
            "phone_number": "77123456",
            "email": "test@example.com",
            "password": "Password@123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.verified = True
        self.user.save()
        self.valid_payload = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        self.unverified_user_data = {
            "name": "Unverified User",
            "phone_number": "77012345",
            "email": "unverified@example.com",
            "password": "Password@123",
        }
        self.unverified_user = User.objects.create_user(**self.unverified_user_data)
        self.url = reverse("authApi:login-api")

    def test_login_view_success(self) -> None:
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Login success.")
        self.assertIn("tokens", response.data)

    def test_login_view_unverified_user(self) -> None:
        unverified_payload = {
            "email": self.unverified_user_data["email"],
            "password": self.unverified_user_data["password"],
        }
        response = self.client.post(self.url, data=unverified_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["status"], "fail")
        self.assertEqual(response.data["message"], "Please confirm your address email.")

    def test_login_view_invalid_credentials(self) -> None:
        invalid_payload = {
            "email": self.valid_payload["email"],
            "password": "WrongPassword",
        }
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "fail")
        self.assertEqual(response.data["message"], "The email or password is incorrect.")
