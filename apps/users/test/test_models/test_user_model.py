from typing import Tuple

import pytest

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    @classmethod
    def setup_class(cls) -> None:
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

    @pytest.fixture
    def create_user(self) -> Tuple[User, User, int]:
        count_of_users = User.objects.count()
        user = User.objects.create_user(**self.user_data)
        superuser = User.objects.create_superuser(**self.superuser_data)
        return user, superuser, count_of_users

    def test_create_user(self, create_user: Tuple[User, User, int]) -> None:
        user, _, count_of_users = create_user
        assert user.email == self.user_data["email"]
        assert user.phone_number == "+253" + self.user_data["phone_number"]
        assert user.name == self.user_data["name"]
        assert user.is_active is True
        assert user.verified is False
        assert user.is_staff is False
        assert user.is_superuser is False
        assert User.objects.count() == count_of_users + 2

    def test_create_superuser(self, create_user: Tuple[User, User, int]) -> None:
        _, superuser, count_of_users = create_user
        assert superuser.email == self.superuser_data["email"]
        assert superuser.phone_number == "+253" + self.superuser_data["phone_number"]
        assert superuser.name == self.superuser_data["name"]
        assert superuser.is_active is True
        assert superuser.verified is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert User.objects.count() == count_of_users + 2

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password", is_superuser=False
            )
