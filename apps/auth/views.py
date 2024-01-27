from typing import Any, Dict, Mapping, Tuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.auth.services import AuthService
from apps.auth.types import ActivationLinkPayloadType


class ActivationView(View):
    template_name: str = "auth/activation-success.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> HttpResponse:
        """
        Retrieves the activation link from the request's keyword arguments and validates it to activate the user.

        Args:
            request (HttpRequest): The HTTP request object.
            *args (Tuple[Any, ...]): Variable length argument list.
            **kwargs (Dict[str, Any]): Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
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
