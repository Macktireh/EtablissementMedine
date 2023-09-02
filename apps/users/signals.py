from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Address


@receiver(post_save, sender=get_user_model(), dispatch_uid="create_user_profile_signal")
def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created:
        Address.objects.create(user=instance)
