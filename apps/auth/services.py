from random import randint

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext as _

from apps.auth.models import Code, User
from apps.auth.tokens import TokenType, getTokensUser, tokenGenerator
from apps.base.exceptions import (
    EmailOrPasswordIncorrectError,
    TokenError,
    UserNotFoundError,
    UserNotVerifiedError,
)
from apps.base.sender import sendEmail, sendSMS


class AuthService:

    @staticmethod
    def signup_email(request: HttpRequest, user: User) -> None:
        token = tokenGenerator.make_token(user)
        domain = get_current_site(request)
        subject = f"Activation du compte sur {domain}"
        context = {
            "user": user,
            "domain": domain,
            "uidb64": urlsafe_base64_encode(force_bytes(user.public_id)) or None,
            "token": token,
        }
        sendEmail(
            subject=subject,
            context=context,
            to=[user.email],
            template_name="auth/mail/activation.html",
        )

    @staticmethod
    def signup_sms(request: HttpRequest, user: User) -> None:
        token = "123456" if settings.ENV == "developement" else randint(100000, 1000000)
        body = _(
            "Voici votre code EtablissementMedine: %(code)d. Ne le partager jamais."
        ) % {"code": token}

        sendSMS(to=user.phone_number, body=body)

        Code.objects.create(
            code=token, user=user, timestamp_requested=timezone.now(), verified=False
        )

    @staticmethod
    def activate_user(request: HttpRequest, uidb64: str, token: str) -> None:
        try:
            public_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            user = None

        if not user:
            raise UserNotFoundError("User not found")

        if not tokenGenerator.check_token(user, token):
            raise TokenError("Invalid token")

        if not user.verified:
            user.verified = True
            user.save()
            domain = get_current_site(request)
            context = {
                "user": user,
                "domain": domain,
            }
            sendEmail(
                subject=_("%(domain)d - Votre compte a est activer")
                % {"domain": domain},
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )

    @staticmethod
    def login(request: HttpRequest, email: str, password: str) -> TokenType:
        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise EmailOrPasswordIncorrectError("Email or password incorrect")

        if not user.verified:
            raise UserNotVerifiedError("User not verified")

        user.last_login = timezone.now()
        user.save()
        return getTokensUser(user)
