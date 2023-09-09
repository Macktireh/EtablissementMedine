from typing import Any

from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.products import utils


class GroupCategory(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[200, 200], null=True, blank=True, upload_to=utils.thumbnail_path_category
    )

    class Meta:
        db_table = "group_category"
        verbose_name = _("Group Category")
        verbose_name_plural = _("Groups Categories")

    def __str__(self) -> str:
        return self.name

    @property
    def thumbnail_preview(self) -> Any:
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="40" height="40" />')
        return ""


class Category(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[200, 200], null=True, blank=True, upload_to=utils.thumbnail_path_category
    )
    group = models.ForeignKey(
        GroupCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="categories"
    )

    class Meta:
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


class Promotion(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    title = models.CharField(_("title of promotion"), max_length=255)
    discount = models.IntegerField(
        _("discount"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = "promotion"
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")
        ordering = ("-start_date",)

    def is_expired_discount(self) -> bool:
        return self.end_date < timezone.now()

    def __str__(self) -> str:
        return "%s" % self.title


class Color(models.Model):
    name = ColorField(_("color"), null=True, blank=True)

    class Meta:
        db_table = "color"
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self) -> str:
        return self.name

    @property
    def color_preview(self) -> Any:
        if self.name:
            return mark_safe(f'<div style="background-color:{self.name}; width:20px; height:20px"></div>')
        return mark_safe('<div style="background-color:transparent; width:20px; height:20px"></div>')


class Product(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    stock = models.PositiveIntegerField(_("stock quantity"), null=False, blank=False, default=0)
    price = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    description = models.TextField(_("description"), null=True, blank=True)
    color = models.ManyToManyField(Color, related_name="products")
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[500, 500], null=True, blank=True, upload_to=utils.thumbnail_path_product
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True
    )
    promotion = models.ForeignKey(
        "Promotion", on_delete=models.SET_NULL, related_name="products", null=True, blank=True
    )

    class Meta:
        db_table = "product"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    @property
    def thumbnail_preview(self) -> Any:
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="50" height="50" />')
        return ""

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    image = ResizedImageField(
        _("thumbnail"), size=[700, 700], null=True, blank=True, upload_to=utils.thumbnail_path_product
    )

    class Meta:
        db_table = "product_image"
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self) -> str:
        return self.product.name

    @property
    def image_preview(self) -> Any:
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""


class ProductAdvertising(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="advertising")

    class Meta:
        db_table = "product_advertising"
        verbose_name = _("Product Advertising")
        verbose_name_plural = _("Product Advertising")

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if ProductAdvertising.objects.count() >= 2:
            raise ValidationError(_("The maximum number of rows in the AdvertisingProducts table is 10."))
        super().save(*args, **kwargs)
