from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import IndexedTimeStampedModel, PublicIdModel
from apps.users.models import User


class PaymentStatusChoices(models.TextChoices):
    AWAITING = "awaiting", _("Awaiting")
    SUCCESSFUL = "successful", _("Successful")
    FAILED = "failed", _("Failed")


class PaymentTypeChoices(models.TextChoices):
    CASH = "cash", _("Cash")
    CREDIT_CARD = "credit_card", _("Credit card")


class Payment(PublicIdModel, IndexedTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    type = models.CharField(
        _("payment type"), max_length=20, choices=PaymentTypeChoices.choices, default=PaymentTypeChoices.CASH
    )
    payment_status = models.CharField(
        _("payment status"),
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.AWAITING,
        db_index=True,
    )
    payment_date = models.DateTimeField(_("payment date"), blank=True, null=True, db_index=True)

    class Meta:
        db_table = "payment"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        if self.payment_status == PaymentStatusChoices.SUCCESSFUL:
            return f"✅ {self.payment_status}"
        elif self.payment_status == PaymentStatusChoices.FAILED:
            return f"❌ {self.payment_status}"
        return f"⏳ {self.payment_status}"
