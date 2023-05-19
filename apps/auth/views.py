from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.auth.services import AuthService
from apps.auth.types import ActivationLinkPayloadType


class ActivationView(View):
    template_name: str = "auth/activation-success.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> HttpResponse:
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        if not uidb64 or not token:
            return render(request, "error/404.html", self.context)

        payload = ActivationLinkPayloadType(uidb64=uidb64, token=token)

        try:
            AuthService.activate_user_link(request, payload)
        except Exception:
            return render(request, "error/404.html", self.context)

        return render(request, self.template_name, self.context)
