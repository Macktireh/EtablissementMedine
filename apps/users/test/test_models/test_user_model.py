from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password',
        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email='')

        with self.assertRaises(TypeError):
            User.objects.create_user(phone_number='')

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertEqual(superuser.phone_number, self.user_data['phone_number'])
        self.assertEqual(superuser.first_name, self.user_data['first_name'])
        self.assertEqual(superuser.last_name, self.user_data['last_name'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser@example.com',
                password='password',
                is_superuser=False
            )
