from django.urls import path

from apps.core.method import getList, getRetrieve
from apps.products.api.views import CategoryListView, ProductAPIView

app_name = "productsApi"

urlpatterns = [
    path("", ProductAPIView.as_view(getList), name="list-products-api"),
    path("<str:public_id>/", ProductAPIView.as_view(getRetrieve), name="retrieve-products-api"),
    path("categories/all/", CategoryListView.as_view(getList), name="list-categories-api"),
]
