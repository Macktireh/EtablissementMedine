from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Product, ProductImage


@receiver(post_save, sender=Product)
def create_product_image(sender, instance: Product, created: bool, **kwargs) -> None:
    if created and instance.thumbnail:
        ProductImage.objects.create(product=instance, image=instance.thumbnail)
