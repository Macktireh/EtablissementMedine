from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestSignUpAPIView(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.client = APIClient()
        self.valid_payload = {
            "name": "Test User",
            "phoneNumber": "77123456",
            "email": "test@example.com",
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }
        self.url = reverse("authApi:signup-api")

    def test_signup_view_success(self) -> None:
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Your account has been successfully registered.")
        self.assertTrue(User.objects.filter(email=self.valid_payload["email"]).exists())
        self.assertTrue(User.objects.filter(phone_number=f"+253{self.valid_payload['phoneNumber']}").exists())

    def test_signup_view_with_invalid_data(self) -> None:
        invalid_payload = self.valid_payload.copy()
        invalid_payload["confirmPassword"] = "DifferentPassword"
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_view_user_already_exists(self) -> None:
        valid_payload = self.valid_payload.copy()
        phone_number = valid_payload["phoneNumber"]
        del valid_payload["confirmPassword"]
        del valid_payload["phoneNumber"]
        valid_payload["phone_number"] = phone_number
        User.objects.create_user(**valid_payload)
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_view_with_mobile_client(self) -> None:
        mobile_payload = self.valid_payload.copy()
        mobile_payload["phoneNumber"] = "77012345"
        response = self.client.post(self.url + "?client=mobile", data=mobile_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Your account has been successfully registered.")
        self.assertTrue(User.objects.filter(email=mobile_payload["email"]).exists())
        self.assertTrue(User.objects.filter(phone_number=f"+253{mobile_payload['phoneNumber']}").exists())
