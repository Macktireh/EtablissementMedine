from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.core.models import AbstractCreatedUpdatedMixin, AbstractPublicIdMixin
from apps.products.utils import thumbnail_path


class GroupCategory(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[200, 200], null=True, blank=True, upload_to=thumbnail_path, force_format="PNG"
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
        _("thumbnail"), size=[200, 200], null=True, blank=True, upload_to=thumbnail_path, force_format="PNG"
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

    # @property
    # def discounted_price(self) -> float:
    #     return self.product.price * (100 - self.discount) / 100

    def is_expired_discount(self) -> bool:
        return self.end_date < timezone.now()

    def __str__(self) -> str:
        return "%s" % self.title


class Product(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    stock = models.PositiveIntegerField(_("stock quantity"), null=False, blank=False, default=0)
    price = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    description = models.TextField(_("description"), null=True, blank=True)
    thumbnail = ResizedImageField(
        _("thumbnail"), size=[400, 400], null=True, blank=True, upload_to=thumbnail_path
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
            return mark_safe(f'<img src="{self.thumbnail}" width="100" height="100" />')
        return mark_safe('<img src="/static/global/images/favicon.png" width="100" height="100" />')
        # return mark_safe(f'<img src="{"https://picsum.photos/100/100"}" width="100" height="100" />')

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(AbstractPublicIdMixin, AbstractCreatedUpdatedMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    image = models.ImageField(_("image"), upload_to=thumbnail_path)

    class Meta:
        db_table = "product_image"
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


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
        """The number of rows in the ProductAdvertising table is 10. If there are more than 10 rows, an exception is thrown."""
        if ProductAdvertising.objects.count() >= 2:
            raise ValidationError("The number of rows in the ProductAdvertising table is 10.")
        super().save(*args, **kwargs)
