from django.contrib import admin
from django.urls import include, path

routes_admin = [
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]


routes_web = [
    path("", include("apps.home.urls")),
    path("auth/user/", include("apps.auth.urls")),
    path("products/", include("apps.products.urls")),
]


urlpatterns = routes_admin + routes_web
