from django.urls import path

from apps.core.method import getList, getRetrieve
from apps.product.api.views import CategoryView, ProductView

app_name = "productApi"

urlpatterns = [
    path("", ProductView.as_view(getList), name="list-products-api"),
    path("<str:publicId>/", ProductView.as_view(getRetrieve), name="retrieve-products-api"),
    path("categories/all/", CategoryView.as_view(getList), name="list-categories-api"),
    path("categories/<str:publicId>", CategoryView.as_view(getRetrieve), name="retrieve-categories-api"),
]
