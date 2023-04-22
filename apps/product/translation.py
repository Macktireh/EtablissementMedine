from modeltranslation.translator import register, TranslationOptions

from apps.product.models import  Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):

    fields = ('name',)


@register(Product)
class AddressTranslationOptions(TranslationOptions):
    
    fields = ('name', 'description',)
