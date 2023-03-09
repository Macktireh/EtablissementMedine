from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.views.auth import SignupView, ActivationView, LoginView, RequestResetPasswordView, ResetPasswordView
from apps.base.method import postCreate


urlpatterns = [
    path('signup/', SignupView.as_view(postCreate), name='signup'),
    path('account/activation/', ActivationView.as_view(postCreate), name='activate'),
    path('login/', LoginView.as_view(postCreate), name='login'),
    path('request/reset-password/', RequestResetPasswordView.as_view(postCreate), name='reset-password-send-email'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(postCreate), name='reset-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='verify-jwt'),
]