from django.urls import path

from apps.users.api.views import AddressView, CurrentUserView

app_name = "userApi"

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="me"),
    path("me/details/", AddressView().as_view(), name="me-address"),
]
