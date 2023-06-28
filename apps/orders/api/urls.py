from django.urls import path

from apps.core.method import getList

# from apps.orders.api.views import CartView, OrderDetailView, ShoppingCartView

app_name = "shoppingApi"


urlpatterns = [
    # path("carts/", CartView.as_view(getList), name="carts-list-api"),
    # path("add-to-cart/", ShoppingCartView.as_view(), name="add-to-cart-api"),
    # path("order-detail/<str:orderPublicId>", OrderDetailView.as_view(), name="order-detail-api"),
]
