from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.auth.views import SignUpView, ActivationView, SignInView, RequestResetPasswordView, ResetPasswordView


app_name = 'auth'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activation/', ActivationView.as_view(), name='activation'),
    path('login/', SignInView.as_view(), name='login'),
    path('request/reset-password/', RequestResetPasswordView.as_view(), name='request-reset-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='verify'),
]