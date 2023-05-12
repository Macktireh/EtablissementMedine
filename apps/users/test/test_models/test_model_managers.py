import pytest

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:

    @classmethod
    def setup_class(cls) -> None:
        cls.user_data = {
            "email": "test@example.com",
            "phone_number": "77123456",
            "name": "John Doe",
            "password": "password",
        }

    def test_create_user(self) -> None:
        user = User.objects.create_user(**self.user_data)
        assert user.email == self.user_data["email"]
        assert user.phone_number == "+253" + self.user_data["phone_number"]
        assert user.name == self.user_data["name"]
        assert user.is_active is True
        assert user.verified is False
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self) -> None:
        superuser = User.objects.create_superuser(**self.user_data)
        assert superuser.email == self.user_data["email"]
        assert superuser.phone_number == "+253" + self.user_data["phone_number"]
        assert superuser.name == self.user_data["name"]
        assert superuser.is_active is True
        assert superuser.verified is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password", is_superuser=False
            )
