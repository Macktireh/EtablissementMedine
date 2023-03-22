from typing import Union

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from apps.auth.managers import UserManager
from apps.base.models import AbstractPublicIdMixin
from apps.auth.tokens import tokenGenerator


class User(AbstractPublicIdMixin, AbstractUser):

    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(_('phone number'), max_length=24, unique=True, db_index=True)
    verified = models.BooleanField(_("verified"), default=False, help_text=_("Designates whether this user has been verified."))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta(AbstractUser.Meta, AbstractPublicIdMixin.Meta):
        db_table = 'users'
    
    @classmethod
    def get_user_by_uidb64(cls, uidb64: str) -> Union['User', None]:
        try:
            public_id = force_str(urlsafe_base64_decode(uidb64))
            return cls.objects.get(public_id=public_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def activate_user(cls, uidb64: str, token: str) -> tuple[Union['User', None], bool, bool]:
        user = cls.get_user_by_uidb64(uidb64)
        if user is None:
            return None, False, False
        return user, tokenGenerator.check_token(user, token), user.verified

    def __str__(self) -> str:
        return f'{self.get_full_name()} <{self.email}>'


class Codes(models.Model):

    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False, db_index=True)
    timestamp_requested = models.DateTimeField(auto_now_add=True)
    timestamp_verified = models.DateTimeField(null=True)

    class Meta:
        db_table = 'codes'
        verbose_name = _('verification code')
        verbose_name_plural = _('verification codes')

    def __str__(self) -> str:
        return self.code
