from django.urls import path

from apps.cart.api import views
from apps.core.method import getList

app_name = "shoppingApi"


urlpatterns = [
    path("get/", views.CartListView.as_view(getList), name="carts-list-api"),
    path("add-to-cart/", views.AddToCartView.as_view(), name="add-to-cart-api"),
    path(
        "update-order-item-quantity/",
        views.UpdateOrderItemQuantityView.as_view(),
        name="update-order-item-quantity-api",
    ),
    path("delete-to-cart/<str:orderItemPublicId>/", views.DeleteToCartView.as_view(), name="delete-to-cart-api"),
    path("clear/", views.ClearCartView.as_view(), name="clear-cart-api"),
]
