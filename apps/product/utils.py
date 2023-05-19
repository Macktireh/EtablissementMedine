def thumbnail_path(instance, filename) -> str:
    from apps.product.models import Product

    if isinstance(instance, Product):
        return f"products/{instance.category.slug}/{instance.slug}.{filename.split('.')[-1]}"
    return f"categories/{instance.slug}.{filename.split('.')[-1]}"
