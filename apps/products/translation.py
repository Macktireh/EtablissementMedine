from modeltranslation.translator import TranslationOptions, register

from apps.products.models import Category, GroupCategory, Product


@register(GroupCategory)
class GroupCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )
