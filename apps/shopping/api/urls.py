from django.urls import path

from apps.base.method import getList
from apps.shopping.api.views import CartView, OrderDetailView, ShoppingCartView


urlpatterns = [
    path('carts/', CartView.as_view(getList), name='carts-list-api'),
    path('add-to-cart/', ShoppingCartView.as_view(), name='add-to-cart-api'),
    path('order-detail/<str:orderPublicId>', OrderDetailView.as_view(), name='order-detail-api'),
]