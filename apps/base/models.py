
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.utils import uidGenerator


class AbstractPublicIdMixin(models.Model):

    public_id = models.CharField(max_length=64, unique=True, null=False, blank=False, editable=False, db_index=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs) -> None:
        if not self.public_id:
            self.public_id = uidGenerator()
        super().save(*args, **kwargs)


class AbstractCreatedUpdatedMixin(models.Model):

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)