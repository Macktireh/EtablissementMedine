from django.contrib import admin
from django.urls import include, path

from config.swagger import schema_view


urlpatterns = [
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    path('', include("apps.home.urls")),
    path('api/v1/auth/user/', include("apps.auth.urls", namespace="auth")),

    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
