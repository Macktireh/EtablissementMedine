from django.urls import path

from apps.auth.views import ActivationView


app_name = 'auth'

urlpatterns = [
    path('activation/<uidb64>/<token>/', ActivationView.as_view(), name='activation'),
]
