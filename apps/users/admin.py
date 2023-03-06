from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('public_id','first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('date_joined', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    readonly_fields = ('public_id', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number',)
    ordering = ('-date_joined',)
