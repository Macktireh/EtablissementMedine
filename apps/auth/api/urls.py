from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView, TokenVerifyView

from apps.auth.api.views import (
    ActivationWithLinkView,
    LoginView,
    LogoutView,
    RequestResetPasswordView,
    ResetPasswordView,
    SignUpView,
)

app_name = "authApi"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup-api"),
    path("activation/", ActivationWithLinkView.as_view(), name="activation-api"),
    path("login/", LoginView.as_view(), name="login-api"),
    path(
        "request/reset-password/",
        RequestResetPasswordView.as_view(),
        name="request-reset-password-api",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password-api",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-api"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="verify-api"),
    path("logout/", TokenBlacklistView.as_view(), name="logout-api"),
]
