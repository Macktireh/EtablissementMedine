from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cart.models import Cart


@receiver(post_save, sender=get_user_model())
def create_cart(sender, instance, created, **kwargs) -> None:
    if created and not Cart.objects.filter(user=instance).exists():
        Cart.objects.create(user=instance)
