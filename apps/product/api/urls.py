from django.urls import path

from apps.core.method import getList
from apps.product.api.views import CategoryView, ProductView

urlpatterns = [
    path("", ProductView.as_view(getList), name="list-products-api"),
    path("categories", CategoryView.as_view(getList), name="list-categories-api"),
]
