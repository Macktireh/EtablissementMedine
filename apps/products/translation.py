from modeltranslation.translator import TranslationOptions, register

from apps.products.models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )
