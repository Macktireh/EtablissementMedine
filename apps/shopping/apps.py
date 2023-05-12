from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShoppingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shopping"
    verbose_name = _("Shopping")
