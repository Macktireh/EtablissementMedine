def thumbnail_path_category(instance, filename) -> str:
    return f"categories/{instance.slug}.{filename.split('.')[-1]}"


def thumbnail_path_product(instance, filename) -> str:
    return f"products/{instance.category.slug}/{instance.slug}.{filename.split('.')[-1]}"
