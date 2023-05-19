from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.customer"
    verbose_name = _("Information about customers")

    def ready(self) -> None:
        import apps.customer.signals
