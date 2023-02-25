from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager
from apps.utils.functions import uidGenerator


class User(AbstractUser):

    username = None
    public_id = models.CharField(max_length=64, unique=True, null=False, blank=False)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    phone_number = models.CharField(_('phone number'), max_length=16, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if not self.public_id:
            self.public_id = uidGenerator()
        super().save(*args, **kwargs)
