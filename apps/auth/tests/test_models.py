from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from apps.auth.models import CodeChecker
from apps.users.models import User


class TestCodeCheckerModel(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.user_data = {
            "email": "user@example.com",
            "phone_number": "77123456",
            "name": "lamda user",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.code_checker_data = {
            "token": "123456",
            "user": self.user,
            "verified": False,
        }

    def test_create_code_checker(self) -> None:
        code_checker = CodeChecker.objects.create(**self.code_checker_data)
        self.assertEqual(code_checker.user, self.user)
        self.assertEqual(code_checker.token, self.code_checker_data["token"])
        self.assertFalse(code_checker.verified)

    def test_code_checker_str_representation(self) -> None:
        code_checker = CodeChecker.objects.create(**self.code_checker_data)
        self.assertEqual(str(code_checker), self.code_checker_data["token"])

    def test_create_token(self) -> None:
        token = CodeChecker.create_token(self.user)
        code_checker = CodeChecker.objects.get(user=self.user)
        self.assertEqual(code_checker.token, token)
        self.assertEqual(code_checker.timestamp_requested.date(), timezone.now().date())
        self.assertFalse(code_checker.verified)

    def test_confirm_verification(self) -> None:
        code_checker = CodeChecker.objects.create(**self.code_checker_data)
        self.assertFalse(code_checker.verified)
        self.assertIsNone(code_checker.timestamp_verified)
        token = self.code_checker_data["token"]
        self.assertTrue(code_checker.confirm_verification(token))
        self.assertIsNotNone(code_checker.timestamp_verified)

        # Test invalid token
        self.assertFalse(code_checker.confirm_verification("invalid_token"))

    def test_is_expired(self) -> None:
        code_checker = CodeChecker.objects.create(**self.code_checker_data)
        code_checker.timestamp_requested = timezone.now() - timezone.timedelta(minutes=30)
        code_checker.save()
        self.assertTrue(code_checker.is_expired())

        code_checker.timestamp_requested = timezone.now() + timezone.timedelta(minutes=30)
        code_checker.save()
        self.assertFalse(code_checker.is_expired())

    def test_get_expiration_time(self) -> None:
        code_checker = CodeChecker.objects.create(**self.code_checker_data)
        expected_expiration = code_checker.timestamp_requested + timezone.timedelta(
            minutes=settings.PHONENUMBER_EXPIRATION
        )
        self.assertEqual(code_checker.get_expiration_time(), expected_expiration)
