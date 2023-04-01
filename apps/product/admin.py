from django.contrib import admin

from apps.product.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('public_id', 'name', 'slug',)
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('public_id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'thumbnail_preview', 'price', 'stock', '_description', 'category', 'created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': ('public_id', 'name', 'slug', 'price', 'stock', 'description', 'thumbnail', 'thumbnail_preview', 'category',)
        }),
    )
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('public_id', 'thumbnail_preview',)
    list_per_page = 10

    def _description(self, obj):
        if len(obj.description) > 90:
            return obj.description[:90] + '...'
        return obj.description
