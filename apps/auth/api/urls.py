from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView, TokenVerifyView

from apps.auth.api.views import (
    ActivationAPIView,
    LoginAPIView,
    RequestActivationAPIView,
    RequestResetPasswordAPIView,
    ResetPasswordAPIView,
    SignUpAPIView,
)

app_name = "authApi"

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup-api"),
    path("activation/", ActivationAPIView.as_view(), name="activation-api"),
    path("request/activation/", RequestActivationAPIView.as_view(), name="request-activation-api"),
    path("login/", LoginAPIView.as_view(), name="login-api"),
    path(
        "request/reset-password/",
        RequestResetPasswordAPIView.as_view(),
        name="request-reset-password-api",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordAPIView.as_view(),
        name="reset-password-api",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-api"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify-api"),
    path("logout/", TokenBlacklistView.as_view(), name="logout-api"),
]
