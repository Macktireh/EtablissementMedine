from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.auth.utils import make_token
from apps.users.models import User


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("user")
        verbose_name_plural = _("users")


class CodeChecker(models.Model):
    token = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(_("verified"), default=False, db_index=True)
    timestamp_requested = models.DateTimeField(_("timestamp requested"), auto_now_add=True)
    timestamp_verified = models.DateTimeField(_("timestamp verified"), null=True)

    class Meta:
        db_table = "code_checker"
        verbose_name = _("code checker")
        verbose_name_plural = _("code checkers")

    def __str__(self) -> str:
        return self.token

    @classmethod
    def create_token(cls, user: User) -> str:
        token = make_token(user)
        obj, created = cls.objects.get_or_create(user=user)
        if not created:
            obj.timestamp_verified = None
            obj.verified = False
        obj.timestamp_requested = timezone.now()
        obj.token = token
        obj.save()
        return token

    def confirm_verification(self, token: str) -> bool:
        if self.token == token:
            self.verified = True
            self.timestamp_verified = timezone.now()
            self.save()
            return True
        return False

    def is_expired(self) -> bool:
        return self.get_expiration_time() < timezone.now()

    def get_expiration_time(self) -> datetime:
        return self.timestamp_requested + timedelta(minutes=settings.PHONENUMBER_EXPIRATION)
