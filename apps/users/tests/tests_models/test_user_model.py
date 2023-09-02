from django.test import TestCase

from apps.users.models import User


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "email": "user@example.com",
            "phone_number": "77123456",
            "name": "lamda user",
            "password": "password",
        }
        cls.superuser_data = {
            "email": "superuser@example.com",
            "phone_number": "77012345",
            "name": "lamda superuser",
            "password": "password",
        }

    def test_create_user(self) -> None:
        count_of_users = User.objects.count()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.phone_number, "+253" + self.user_data["phone_number"])
        self.assertEqual(user.name, self.user_data["name"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(User.objects.count(), count_of_users + 1)

    def test_create_superuser(self) -> None:
        count_of_users = User.objects.count()
        superuser = User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(superuser.email, self.superuser_data["email"])
        self.assertEqual(superuser.phone_number, "+253" + self.superuser_data["phone_number"])
        self.assertEqual(superuser.name, self.superuser_data["name"])
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.verified)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(User.objects.count(), count_of_users + 1)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password", is_superuser=False
            )

    def test_user_str_representation(self) -> None:
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{user.name} <{user.email}>"
        self.assertEqual(str(user), expected_str)
