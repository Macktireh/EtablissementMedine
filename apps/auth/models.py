from typing import Union

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from apps.auth.managers import UserManager
from apps.auth.tokens import tokenGenerator
from apps.base.models import AbstractPublicIdMixin


class User(AbstractPublicIdMixin, AbstractUser):
    username = None
    fisrt_name = None
    last_name = None
    name = models.EmailField(_("name"), max_length=128, blank=True, null=True)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, db_index=True
    )
    phonenumber = models.CharField(
        _("phone number"), max_length=24, unique=True, db_index=True
    )
    verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether this user has been verified."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta(AbstractUser.Meta, AbstractPublicIdMixin.Meta):
        db_table = "user"

    @classmethod
    def activate_user(cls, uidb64: str, token: str) -> tuple["User" | None, bool, bool]:
        try:
            public_id = force_str(urlsafe_base64_decode(uidb64))
            user = cls.objects.get(public_id=public_id)
        except cls.DoesNotExist:
            user = None

        return user, tokenGenerator.check_token(user, token), user.verified

    def __str__(self) -> str:
        return f"{self.get_full_name()} <{self.email}>"


class Code(models.Model):
    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(_("verified"), default=False, db_index=True)
    timestamp_requested = models.DateTimeField(
        _("timestamp requested"), auto_now_add=True
    )
    timestamp_verified = models.DateTimeField(_("timestamp verified"), null=True)

    class Meta:
        db_table = "code"
        verbose_name = _("verification code")
        verbose_name_plural = _("verification codes")

    def __str__(self) -> str:
        return self.code
