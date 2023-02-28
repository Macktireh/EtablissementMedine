from django.contrib.auth.apps import AuthConfig
from django.utils.translation import gettext_lazy as _


class AuthConfigApps(AuthConfig):
    verbose_name = _("Authorization")
