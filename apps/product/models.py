from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.product.utils import thumbnail_path


class Category(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[200, 200], null=True, blank=True, upload_to=thumbnail_path, force_format="PNG"
    )

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        db_table = "category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name

    @property
    def thumbnail_preview(self) -> Any:
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="40" height="40" />')
        return ""

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    stock = models.PositiveIntegerField(_("stock quantity"), null=False, blank=False, default=0)
    price = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    discount = models.IntegerField(
        _("discount"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False,
    )
    price_discount = models.DecimalField(
        _("price discount"), max_digits=10, decimal_places=2, null=False, blank=False
    )
    # Expiry date Discount :
    expiry_date_discount = models.DateTimeField(_("expiry date discount"), null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[400, 400], null=True, blank=True, upload_to=thumbnail_path
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True
    )

    class Meta(AbstractPublicIdMixin.Meta, AbstractCreatedUpdatedMixin.Meta):
        db_table = "product"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    @property
    def thumbnail_preview(self) -> Any:
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail}" width="100" height="100" />')
        return ""
        # return mark_safe(f'<img src="{"https://picsum.photos/100/100"}" width="100" height="100" />')

    def is_expired_discount(self) -> bool:
        if not self.expiry_date_discount:
            return False
        return self.expiry_date_discount < timezone.now()

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        self.price_discount = self.price * (100 - self.discount) / 100
        super().save(*args, **kwargs)
