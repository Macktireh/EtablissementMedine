from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager
from apps.base.models import AbstractPublicIdMixin
from apps.base.functions import uidGenerator


class User(AbstractPublicIdMixin, AbstractUser):

    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    phone_number = models.CharField(_('phone number'), max_length=16, unique=True)
    is_verified = models.BooleanField(_("verified"), default=False, help_text=_("Designates whether this user has been verified."))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta(AbstractUser.Meta, AbstractPublicIdMixin.Meta):
        db_table = 'users'

    def __str__(self) -> str:
        return self.email