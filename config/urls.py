from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from apps.core.swagger import schema_view

urlpatterns_admin = [
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
]


urlpatterns_web = [
    path("", include("apps.home.urls")),
    path("auth/user/", include("apps.auth.urls")),
]


urlpatterns_api_v1 = [
    path("api/v1/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-redoc"),
    path("api/v1/auth/user/", include("apps.auth.api.urls")),
    path("api/v1/user/", include("apps.users.api.urls")),
    path("api/v1/products/", include("apps.product.api.urls")),
    path("api/v1/shopping/", include("apps.shopping.api.urls")),
]


urlpatterns_api = urlpatterns_api_v1


urlpatterns = i18n_patterns(*urlpatterns_admin, *urlpatterns_web) + urlpatterns_api

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [path("__debug__", include(debug_toolbar.urls))] + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
