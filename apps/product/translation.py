from modeltranslation.translator import TranslationOptions, register

from apps.product.models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class AddressTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )
