from typing import Any

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.base.models import AbstractPublicIdMixin, AbstractCreatedUpdatedMixin


class Category(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):

    name = models.CharField(_('name'), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self) -> str:
        return self.name

    def save(self ,*args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def thumbnail_path (instance, filename) -> str:
    return f"products/{instance.category.slug}/{instance.slug}.{filename.split('.')[-1]}"


class Product(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):

    name = models.CharField(_('name'), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_('slug'), max_length=255, unique=True, db_index=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00)
    stock = models.PositiveIntegerField(_('stock quantity'), null=False, blank=False, default=0)
    description = models.TextField(_('description'), null=True, blank=True)
    thumbnail = models.ImageField(_('thumbnail'), null=True, blank=True, upload_to=thumbnail_path)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self) -> str:
        return self.name
    
    @property
    def thumbnail_preview(self):
        # if self.thumbnail:
        #     return mark_safe(f'<img src="{"https://fastly.picsum.photos/id/845/200/200.jpg?hmac=KMGSD70gM0xozvpzPM3kHIwwA2TRlVQ6d2dLW_b1vDQ"}" width="200" height="200" />')
        # return ""
        return mark_safe(f'<img src="{"https://picsum.photos/100/100"}" width="100" height="100" />')

    def save(self ,*args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
