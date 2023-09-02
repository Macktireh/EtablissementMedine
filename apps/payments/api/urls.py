from django.urls import path

from apps.core.method import getList
from apps.orders.api import views

app_name = "OrdersApi"


urlpatterns = [
    path("orders/", views.OrderView.as_view(getList), name="order-list-api"),
]
