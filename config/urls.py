from django.contrib import admin
from django.urls import include, path

from config.swagger import schema_view


urlpatterns_api_v1 = [
    path('api/v1/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/auth/user/', include("apps.auth.api.urls")),
    path('api/v1/products/', include("apps.product.api.urls")),
    path('api/v1/shopping/', include("apps.shopping.api.urls")),
]

urlpatterns = [
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include("apps.home.urls")),
    path('auth/user/', include("apps.auth.urls")),
] + urlpatterns_api_v1
