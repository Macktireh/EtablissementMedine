from typing import Any, Dict, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractPublicIdMixin
from apps.users.managers import UserManager


class User(AbstractPublicIdMixin, AbstractUser):
    username = None
    fisrt_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=128)
    email = models.EmailField(_("email address"), max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(_("phone number"), max_length=24, unique=True, db_index=True)
    verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether this user has been verified."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    objects = UserManager()

    class Meta(AbstractUser.Meta, AbstractPublicIdMixin.Meta):
        db_table = "user"

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        if not str(self.phone_number).startswith("+253"):
            self.phone_number = "+253" + self.phone_number
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
