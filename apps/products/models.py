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

from apps.core.models import IndexedTimeStampedModel, PublicIdModel
from apps.products import utils


class GroupCategory(PublicIdModel, IndexedTimeStampedModel):
    """Represents a group category."""

    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name of the group category (e.g: 'Electronics')"),
    )
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Slug of the group category (e.g: 'electronics')"),
    )
    thumbnail = ResizedImageField(
        _("thumbnail"),
        size=[200, 200],
        null=True,
        blank=True,
        upload_to=utils.thumbnail_path_category,
        help_text=_("Thumbnail of the group category"),
    )

    class Meta:
        db_table = "groupCategories"
        verbose_name = _("Group Category")
        verbose_name_plural = _("Groups Categories")

    def __str__(self) -> str:
        """
        Returns the string representation of the GroupCategory object.
        """
        return self.name

    @property
    def thumbnail_preview(self) -> str:
        """
        Returns a thumbnail preview of the object.

        This property returns a thumbnail preview of the object if a thumbnail is available.
        The thumbnail is displayed as an HTML `img` tag with the `src` attribute set to the URL of the thumbnail image.
        The width and height of the thumbnail image are set to 40 pixels.

        Returns:
            str: The HTML code for the thumbnail preview if a thumbnail is available,
                            or an empty string if no thumbnail is available.
        """
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="40" height="40" />')
        return ""


class Category(PublicIdModel, IndexedTimeStampedModel):
    """Represents a category."""

    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name of the category (e.g: 'Watches')"),
    )
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, help_text=_("Slug of the category (e.g: 'watches')")
    )
    thumbnail = ResizedImageField(
        _("thumbnail"),
        size=[200, 200],
        null=True,
        blank=True,
        upload_to=utils.thumbnail_path_category,
        help_text=_("Thumbnail of the category"),
    )
    group = models.ForeignKey(
        GroupCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories",
        help_text=_("The group that the category belongs to."),
    )

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        """
        Returns the string representation of the Category object.
        """
        return self.name

    @property
    def thumbnail_preview(self) -> Any:
        """
        Returns a thumbnail preview of the object.

        This property returns a thumbnail preview of the object if a thumbnail is available.
        The thumbnail is displayed as an HTML `img` tag with the `src` attribute set to the URL of the thumbnail image.
        The width and height of the thumbnail image are set to 40 pixels.

        Returns:
            str: The HTML code for the thumbnail preview if a thumbnail is available,
                            or an empty string if no thumbnail is available.
        """
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="40" height="40" />')
        return ""

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """
        Overrides the save method to set the slug and save the object.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Promotion(PublicIdModel, IndexedTimeStampedModel):
    title = models.CharField(
        _("title of promotion"), max_length=255, unique=True, help_text=_("Title of the promotion")
    )
    discount = models.IntegerField(
        _("discount"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False,
        help_text=_("Discount of the promotion"),
    )
    start_date = models.DateTimeField(_("start date"), help_text=_("Start date of the promotion"))
    end_date = models.DateTimeField(_("end date"), help_text=_("End date of the promotion"))

    class Meta:
        db_table = "promotions"
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")
        ordering = ("-start_date",)

    @property
    def is_expired_discount(self) -> bool:
        """Returns True if the discount is expired, False otherwise."""
        return self.end_date < timezone.now()

    def __str__(self) -> str:
        """Returns the string representation of the Promotion object."""
        return self.title


class Color(models.Model):
    """Represents a color."""

    name = ColorField(_("color"), null=True, blank=True, help_text=_("Color of the product"))

    class Meta:
        db_table = "colors"
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self) -> str:
        """Returns the string representation of the Color object."""
        return self.name

    @property
    def color_preview(self) -> str:
        """
        Returns a string representing the color preview of the object.

        Returns:
            str: The HTML code for the color preview div element.
        """
        if self.name:
            return mark_safe(f'<div style="background-color:{self.name}; width:20px; height:20px"></div>')
        return mark_safe('<div style="background-color:transparent; width:20px; height:20px"></div>')


class Product(PublicIdModel, IndexedTimeStampedModel):
    """Represents a product."""

    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name of the product (e.g: 'Apple Watch')"),
    )
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Slug of the product (e.g: 'apple-watch')"),
    )
    stock = models.PositiveIntegerField(
        _("stock quantity"), null=False, blank=False, default=0, help_text=_("Stock quantity of the product")
    )
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.00,
        help_text=_("Price of the product"),
    )
    description = models.TextField(_("description"), null=True, blank=True, help_text=_("Description of the product"))
    color = models.ManyToManyField(
        Color,
        related_name="products",
        blank=True,
        help_text=_("Color of the product"),
        db_table="productColors",
    )
    thumbnail = ResizedImageField(
        _("thumbnail"),
        size=[500, 500],
        null=True,
        blank=True,
        upload_to=utils.thumbnail_path_product,
        help_text=_("Thumbnail of the product"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
        help_text=_("Category of the product"),
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
        help_text=_("The promotion of the product"),
    )

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    @property
    def thumbnail_preview(self) -> str:
        """
        Returns a thumbnail preview of the object.

        This property returns a thumbnail preview of the object if a thumbnail is available.
        The thumbnail is displayed as an HTML `img` tag with the `src` attribute set to the URL of the thumbnail image.
        The width and height of the thumbnail image are set to 40 pixels.

        Returns:
            str: The HTML code for the thumbnail preview if a thumbnail is available,
                            or an empty string if no thumbnail is available.
        """
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="50" height="50" />')
        return ""

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """
        Overrides the save method to set the slug and save the object.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(PublicIdModel, IndexedTimeStampedModel):
    """Represents a product image."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
        help_text=_("Product of the image"),
    )
    image = ResizedImageField(
        _("thumbnail"),
        size=[700, 700],
        null=True,
        blank=True,
        upload_to=utils.thumbnail_path_product,
        help_text=_("Image of the product"),
    )

    class Meta:
        db_table = "productImages"
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self) -> str:
        return self.product.name

    @property
    def image_preview(self) -> str:
        """
        Returns a thumbnail preview of the object.

        This property returns a thumbnail preview of the object if a thumbnail is available.
        The thumbnail is displayed as an HTML `img` tag with the `src` attribute set to the URL of the thumbnail image.
        The width and height of the thumbnail image are set to 40 pixels.

        Returns:
            str: The HTML code for the thumbnail preview if a thumbnail is available,
                            or an empty string if no thumbnail is available.
        """
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""


class ProductAdvertising(PublicIdModel, IndexedTimeStampedModel):
    """Represents a product advertising."""

    title = models.CharField(_("title"), max_length=255, unique=True, help_text=_("Title of the advertising"))
    description = models.TextField(
        _("description"), null=True, blank=True, help_text=_("Description of the advertising")
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="advertising",
        help_text=_("Product of the advertising"),
    )

    class Meta:
        db_table = "productAdvertisings"
        verbose_name = _("Product Advertising")
        verbose_name_plural = _("Product Advertisings")

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """
        Overrides the save method to set the slug and save the object and
        check the maximum number of rows in the AdvertisingProducts table is 10, if it is not the case raise an error
        """
        if not self.slug:
            self.slug = slugify(self.title)
        if ProductAdvertising.objects.count() >= 10:
            raise ValidationError(_("The maximum number of rows in the AdvertisingProducts table is 10."))
        super().save(*args, **kwargs)
