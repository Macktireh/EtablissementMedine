from django.contrib import admin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "payment_status", "payment_date")
