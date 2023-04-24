from datetime import datetime, timedelta
from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.auth.managers import UserManager
from apps.base.models import AbstractPublicIdMixin
from config import settings


class User(AbstractPublicIdMixin, AbstractUser):

    username = None
    fisrt_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=128)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, db_index=True
    )
    phone_number = models.CharField(
        _("phone number"), max_length=24, unique=True, db_index=True
    )
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

    def save(self, *args, **kwargs) -> None:
        if not self.phone_number.startswith("+253") or not self.phone_number.startswith("00253"):
            self.phone_number = "+253" + self.phone_number
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.get_full_name()} <{self.email}>"


class PhoneNumberCheck(models.Model):

    token = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(_("verified"), default=False, db_index=True)
    timestamp_requested = models.DateTimeField(
        _("timestamp requested"), auto_now_add=True
    )
    timestamp_verified = models.DateTimeField(_("timestamp verified"), null=True)

    class Meta:
        db_table = "phoneNumberCheck"
        verbose_name = _("verification code")
        verbose_name_plural = _("verification codes")

    def __str__(self) -> str:
        return self.token

    @classmethod
    def create_token(cls, phone_number: str) -> str:
        token = "123456" if settings.ENV == "developement" else randint(100000, 1000000)
        obj, _ = cls.objects.get_or_create(user__phone_number=phone_number)
        obj.token = token
        obj.timestamp_requested = timezone.now()
        obj.timestamp_verified = None
        obj.verified = False
        obj.save()
        return token

    def confirm_verification(self, token) -> bool:
        if self.token == token:
            self.verified = True
            self.timestamp_verified = timezone.now()
            self.save()
            return True
        return False

    def is_expired(self) -> bool:
        return self.get_expiration_time() < timezone.now()

    def get_expiration_time(self) -> datetime:
        return self.timestamp_requested + timedelta(
            minutes=settings.PHONENUMBER_EXPIRATION
        )
