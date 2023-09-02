from django.db.models.signals import post_save
from django.test import TestCase

from apps.users.models import Address, User
from apps.users.signals import create_user_profile_signal


class TestAddressModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "email": "user@example.com",
            "phone_number": "77123456",
            "name": "lamda user",
            "password": "password",
        }

        # Temporarily disconnect the signal during tests
        post_save.disconnect(
            sender=User, receiver=create_user_profile_signal, dispatch_uid="create_user_profile_signal"
        )

        cls.user = User.objects.create_user(**cls.user_data)
        cls.address_data = {
            "user": cls.user,
            "street_address": "123 Main Street",
            "city": "Cityville",
            "zipcode": "12345",
            "country": "Countryland",
        }

    def tearDown(self) -> None:
        # Reconnect the signal after tests
        post_save.connect(
            sender=User, receiver=create_user_profile_signal, dispatch_uid="create_user_profile_signal"
        )

    def test_create_address(self) -> None:
        address, created = Address.objects.get_or_create(user=self.user, defaults=self.address_data)
        self.assertTrue(created)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.street_address, self.address_data["street_address"])
        self.assertEqual(address.city, self.address_data["city"])
        self.assertEqual(address.zipcode, self.address_data["zipcode"])
        self.assertEqual(address.country, self.address_data["country"])

    def test_address_str_representation(self) -> None:
        address, created = Address.objects.get_or_create(user=self.user, defaults=self.address_data)
        self.assertTrue(created)
        expected_str = f"{address.user.name}"
        self.assertEqual(str(address), expected_str)
