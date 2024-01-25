from django.urls import path

from apps.products.views import ProductView

app_name = "products"

urlpatterns = [
    path("", ProductView.as_view(), name="list"),
]
