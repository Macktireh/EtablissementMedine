from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "authUser"
    verbose_name = _("Authentication and Authorization")
