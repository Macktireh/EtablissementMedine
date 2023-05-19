from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    street_address = models.CharField(_("street address"), max_length=256, blank=True, null=True)
    city = models.CharField(_("City or neighborhood"), max_length=128, blank=True, null=True)
    zipcode = models.CharField(_("Zip / Postal code"), max_length=12, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=64, blank=True, null=True)

    class Meta:
        db_table = "address"
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ["-user__date_joined"]

    def __str__(self) -> str:
        return self.user.name
