from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.auth.services import AuthService


class ActivationView(View):

    template_name: str = "auth/activation-success.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        uidb64: str = kwargs.get("uidb64")
        token: str = kwargs.get("token")

        try:
            AuthService.activate_user(request, uidb64, token)
        except:
            return render(request, "error/404.html", self.context)

        return render(request, self.template_name, self.context)
