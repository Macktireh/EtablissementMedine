from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Address(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(_('address'), max_length=256, blank=True, null=True)
    city = models.CharField(_('City or neighborhood'), max_length=128, blank=True, null=True)
    zipcode = models.CharField(_('Zip / Postal code'), max_length=12, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'addresses'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['-user__date_joined']

    def __str__(self) -> str:
        return self.user.get_full_name()
