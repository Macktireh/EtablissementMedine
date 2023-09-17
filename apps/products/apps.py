from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = _("Products and categories")

    def ready(self) -> None:
        import apps.products.signals  # noqa: F401
