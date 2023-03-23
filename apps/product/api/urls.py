from django.urls import path

from apps.product.api.views import CategoryView, ProductView
from apps.base.method import getList


urlpatterns = [
    path('', ProductView.as_view(getList), name='list-products-api'),
    path('categories', CategoryView.as_view(getList), name='list-categories-api'),
]
