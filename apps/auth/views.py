from typing import Any, Mapping

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.auth.models import User
from apps.base.mail import sendEmail


class ActivationView(View):
    template_name: str = "auth/activation-success.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        uidb64: str = kwargs.get("uidb64")
        token: str = kwargs.get("token")
        domain = get_current_site(request)
        user, check, verified = User.activate_user(uidb64, token)

        if user is None or not check:
            return render(request, "error/404.html", self.context)

        if not verified:
            user.verified = True
            user.save()
            context = {
                "user": user,
                "domain": domain,
            }
            sendEmail(
                subject=f"{domain} - Votre compte a est activer",
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )
        return render(request, self.template_name, self.context)
