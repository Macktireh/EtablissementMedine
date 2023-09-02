from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.auth.api.serializers import (
    LoginSerializer,
    RequestActivationOrResetPasswordSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
)
from apps.users.models import User


class TestLoginSerializer(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.payload = {
            "email": "test@example.com",
            "password": "Password@123",
        }

    def test_login_serializer_is_valid(self) -> None:
        serializer = LoginSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], self.payload["email"])

    def test_login_serializer_is_not_valid(self) -> None:
        serializer = LoginSerializer(data={"email": "test@example.com"})
        self.assertFalse(serializer.is_valid())
        serializer = LoginSerializer(data={"password": "Password@123"})
        self.assertFalse(serializer.is_valid())
        serializer = LoginSerializer(data={"password": "Password@123"})
        self.assertFalse(serializer.is_valid())


class TestSignupSerializer(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.payload = {
            "name": "Test User",
            "phoneNumber": "77123456",
            "email": "test@example.com",
            "password": "Password@123",
            "confirmPassword": "Password@123",
        }

    def test_signup_serializer_is_valid(self) -> None:
        serializer = SignupSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.payload["name"])
        self.assertEqual(serializer.validated_data["phone_number"], self.payload["phoneNumber"])
        self.assertEqual(serializer.validated_data["email"], self.payload["email"])

    def test_signup_serializer_is_not_valid(self) -> None:
        invalid_payload = self.payload.copy()
        invalid_payload["confirmPassword"] = "DifferentPassword"
        serializer = SignupSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("confirmPassword", serializer.errors)

    def test_create_user(self) -> None:
        serializer = SignupSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, self.payload["name"])
        self.assertEqual(user.phone_number, "+253" + self.payload["phoneNumber"])
        self.assertEqual(user.email, self.payload["email"])

    def test_create_user_with_invalid_data(self) -> None:
        invalid_payload = self.payload.copy()
        invalid_payload["confirmPassword"] = "DifferentPassword"
        serializer = SignupSerializer(data=invalid_payload)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            serializer.save()


class TestRequestResetPasswordSerializer(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.payload = {
            "email": "test@example.com",
        }

    def test_request_reset_password_serializer_is_valid(self) -> None:
        serializer = RequestActivationOrResetPasswordSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], self.payload["email"])

    def test_request_reset_password_serializer_is_not_valid(self) -> None:
        invalid_payload = {}
        serializer = RequestActivationOrResetPasswordSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class TestResetPasswordSerializer(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.payload = {
            "password": "NewPassword@123",
            "confirmPassword": "NewPassword@123",
        }

    def test_reset_password_serializer_is_valid(self) -> None:
        serializer = ResetPasswordSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["password"], self.payload["password"])

    def test_reset_password_serializer_is_not_valid(self) -> None:
        invalid_payload = self.payload.copy()
        invalid_payload["confirmPassword"] = "DifferentPassword"
        serializer = ResetPasswordSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("confirmPassword", serializer.errors)
