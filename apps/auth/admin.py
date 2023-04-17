from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.auth.models import Code, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "verified",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "verified",
        "is_active",
        "date_joined",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {"fields": ("public_id", "first_name", "last_name", "phone_number")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "verified",
                    "is_staff",
                ),
            },
        ),
    )
    readonly_fields = ("public_id", "date_joined", "last_login")
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    ordering = ("date_joined",)
    list_per_page = 20

    def has_delete_permission(self, request: HttpRequest, obj: User = None) -> bool:
        return request.user.is_superuser


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "phone_number",
        "verified",
        "timestamp_requested",
        "timestamp_verified",
    )
    search_fields = (
        "code",
        "name",
    )

    def name(self, obj: Code) -> str:
        return obj.user.get_full_name()

    def phone_number(self, obj: Code) -> str:
        return obj.user.phone_number

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("user")

    def has_view_permission(self, request: HttpRequest, obj: Code = None) -> bool:
        return request.user.is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Code = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Code = None) -> bool:
        return False
