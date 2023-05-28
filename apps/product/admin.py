from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from apps.product.models import Category, Product


@admin.register(Category)
class CategoryAdmin(TabbedExternalJqueryTranslationAdmin):
    list_display = (
        "name",
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "public_id",
                    "name",
                    "slug",
                    "thumbnail",
                    "thumbnail_preview",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "slug",
                    "thumbnail",
                ),
            },
        ),
    )
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "public_id",
        "thumbnail_preview",
    )


@admin.register(Product)
class ProductAdmin(TabbedExternalJqueryTranslationAdmin):
    list_display = (
        "name",
        "thumbnail_preview",
        "stock",
        "price",
        "_discount",
        "price_discount",
        "expiry_date_discount",
        "_description",
        "category",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "public_id",
                    "name",
                    "slug",
                    "stock",
                    "price",
                    "discount",
                    "price_discount",
                    "expiry_date_discount",
                    "description",
                    "thumbnail",
                    "thumbnail_preview",
                    "category",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "slug",
                    "stock",
                    "price",
                    "discount",
                    "expiry_date_discount",
                    "description",
                    "thumbnail",
                    "category",
                ),
            },
        ),
    )
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "public_id",
        "thumbnail_preview",
        "price_discount",
    )
    list_per_page = 10

    def _description(self, obj) -> str:
        if len(obj.description) > 30:
            return obj.description[:30] + "..."
        return obj.description

    def _discount(self, obj) -> str:
        if obj.discount:
            return f"-{obj.discount}%"
