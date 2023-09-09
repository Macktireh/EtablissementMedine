from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from apps.products.models import (
    Category,
    Color,
    GroupCategory,
    Product,
    ProductAdvertising,
    ProductImage,
    Promotion,
)


@admin.register(GroupCategory)
class GroupCategoryAdmin(TabbedExternalJqueryTranslationAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
        "thumbnail_preview",
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


@admin.register(Category)
class CategoryAdmin(TabbedExternalJqueryTranslationAdmin):
    list_display = (
        "name",
        "group",
        "created_at",
        "updated_at",
        "thumbnail_preview",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "public_id",
                    "name",
                    "slug",
                    "group",
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
                    "group",
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
    search_fields = ("name",)
    list_filter = ("group",)


@admin.register(Product)
class ProductAdmin(TabbedExternalJqueryTranslationAdmin):
    list_display = (
        "name",
        "_thumbnail",
        "stock",
        "_price",
        "_description",
        "category",
        "promotion",
    )
    list_filter = ("category", "promotion")
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
                    "description",
                    "color",
                    "category",
                    "promotion",
                    "thumbnail",
                    "thumbnail_preview",
                    "created_at",
                    "updated_at",
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
                    "description",
                    "color",
                    "category",
                    "promotion",
                    "thumbnail",
                ),
            },
        ),
    )
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "public_id",
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )
    list_per_page = 10

    def _price(self, obj) -> str:
        if obj.price:
            return f"${obj.price:.2f}"

    def _thumbnail(self, obj: Product) -> str:
        return obj.thumbnail_preview

    def _description(self, obj) -> str:
        if obj.description and len(obj.description) > 30:
            return obj.description[:30] + "..."
        return obj.description


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "_discount",
        "start_date",
        "end_date",
    )

    def _discount(self, obj) -> str:
        if obj.discount:
            return f"-{obj.discount}%"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "_product",
        "image_preview",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "public_id",
                    "product",
                    "image",
                    "image_preview",
                )
            },
        ),
    )
    readonly_fields = (
        "public_id",
        "image_preview",
    )

    def _product(self, obj) -> str:
        return obj.product.name


@admin.register(ProductAdvertising)
class ProductAdvertisingAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color_preview",
    )
