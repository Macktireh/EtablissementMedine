from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include("apps.home.urls")),
]
