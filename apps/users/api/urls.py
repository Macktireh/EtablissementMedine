from django.urls import path

from apps.users.api.views import CurrentUserView

app_name = "user"

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="me"),
]
