from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.customer.models import Address


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        Address.objects.create(user=instance)

