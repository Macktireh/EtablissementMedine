from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.auth.api.views import SignUpView, ActivationView, SignInView, RequestResetPasswordView, ResetPasswordView


# app_name = 'auth'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup-api'),
    path('activation/', ActivationView.as_view(), name='activation-api'),
    path('login/', SignInView.as_view(), name='login-api'),
    path('request/reset-password/', RequestResetPasswordView.as_view(), name='request-reset-password-api'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password-api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-api'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='verify-api'),
]