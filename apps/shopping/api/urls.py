from django.urls import path

from apps.base.method import getList
from apps.shopping.api.views import ShoppingCartView


urlpatterns = [
    path('carts/', ShoppingCartView().as_view(), name='carts-list-api'),
]