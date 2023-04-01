from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.customer.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone_number', 'street_address', 'city', 'zipcode', 'country')

    def name(self, obj: Address) -> str:
        return obj.user.get_full_name()

    def email(self, obj: Address) -> str:
        return obj.user.email

    def phone_number(self, obj: Address) -> str:
        return obj.user.phone_number
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user')
    