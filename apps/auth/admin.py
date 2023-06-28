from typing import cast

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.auth.models import CodeChecker, GroupProxy, UserProxy
from apps.users.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(Group)


@admin.register(GroupProxy)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(UserProxy)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(CodeChecker)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        "token",
        "name",
        "phone_number",
        "verified",
        "timestamp_requested",
        "timestamp_verified",
    )
    search_fields = (
        "token",
        "name",
    )

    def name(self, obj: CodeChecker) -> str:
        return obj.user.get_full_name()

    def phone_number(self, obj: CodeChecker) -> str:
        return obj.user.phone_number

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("user")

    def has_view_permission(self, request: HttpRequest, obj: CodeChecker | None = None) -> bool:
        return cast(UserProxy, request.user).is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: CodeChecker | None = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: CodeChecker | None = None) -> bool:
        return request.user.is_superuser
