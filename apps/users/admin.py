from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.users.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone_number",
        "street_address",
        "city",
        "zipcode",
        "country",
    )
    search_fields = (
        "user__name",
        "user__email",
        "user__phone_number",
        "street_address",
        "city",
        "zipcode",
        "country",
    )

    def name(self, obj: Address) -> str:
        return obj.user.name

    def email(self, obj: Address) -> str:
        return obj.user.email

    def phone_number(self, obj: Address) -> str:
        return obj.user.phone_number

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("user")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Address | None = None) -> bool:
        return request.user.is_superuser
