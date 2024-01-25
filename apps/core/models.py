from typing import Any, Dict, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.utils import uidGenerator


class PublicIdModel(models.Model):
    public_id = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for this object. This is used to identify "),
    )

    class Meta:
        abstract = True

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        if not self.public_id:
            self.public_id = uidGenerator()
        super().save(*args, **kwargs)


class IndexedTimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)

    class Meta:
        abstract = True
