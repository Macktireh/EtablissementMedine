def thumbnail_path(instance, filename) -> str:
    from apps.products.models import ProductImage

    if isinstance(instance, ProductImage):
        return f"products/{instance.category.slug}/{instance.slug}.{filename.split('.')[-1]}"
    return f"categories/{instance.slug}.{filename.split('.')[-1]}"
