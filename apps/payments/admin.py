from django.contrib import admin

from apps.payments.models import Payment


# @admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "payment_status", "payment_date")
