from django.apps import AppConfig
from django.contrib.auth.apps import AuthConfig as BaseAuthConfig
from django.utils.translation import gettext_lazy as _


class AuthUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "authUser"
    verbose_name = _("Authentication and User Management")


class AuthConfig(BaseAuthConfig):
    verbose_name = _("Authorization")
