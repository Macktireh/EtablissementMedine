from typing import Any

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from apps.base.models import AbstractPublicIdMixin, AbstractCreatedUpdatedMixin


class Category(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'categories'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    price = models.FloatField(_('price'), null=False, blank=False, default=0.0)
    stock = models.IntegerField(_('stock quantity'), null=False, blank=False, default=0)
    description = models.TextField(_('description'), null=True, blank=True)
    thumbnail = models.ImageField(_('thumbnail'), null=True, blank=True, upload_to='products/thumbnails')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        db_table = 'products'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
