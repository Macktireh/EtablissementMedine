from django.contrib import admin
from django.contrib.admin.models import CHANGE, DELETION, LogEntry
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext_lazy as _

admin.site.site_title = _("Medine Database Administration")
admin.site.site_header = _("Medine Database Administration")
admin.site.index_title = _("Medine Database Administration")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"
    list_filter = ["content_type", "action_flag"]
    search_fields = ["object_repr", "change_message"]
    list_display = ["action_time", "user", "content_type", "object_link"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: LogEntry = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: LogEntry = None) -> bool:
        return False

    def has_view_permission(self, request: HttpRequest, obj: LogEntry = None) -> bool:
        return request.user.is_superuser

    def object_link(self, obj: LogEntry) -> SafeText:
        if obj.action_flag == DELETION:
            link = '<span class="deletelink">%s</span>' % escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s" class="%s">%s</a>' % (
                reverse("admin:%s_%s_change" % (ct.app_label, ct.model), args=[obj.object_id]),
                "changelink" if obj.action_flag == CHANGE else "addlink",
                escape(obj.object_repr),
            )
        return mark_safe(link)

    object_link.allow_tags = True
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

    def queryset(self, request: HttpRequest):
        return super(LogEntryAdmin, self).queryset(request).prefetch_related("content_type")
