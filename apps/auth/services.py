from random import randint

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext as _

from apps.auth.models import PhoneNumberCheck, User
from apps.auth.tokens import getTokensUser, tokenGenerator
from apps.auth.types import ActivationPayloadType, TokenType
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
        token = PhoneNumberCheck.create_token(user.phone_number)
        body = _(
            "Voici votre code EtablissementMedine: %(token)d. Ne le partager jamais."
        ) % {"token": token}

        sendSMS(to=user.phone_number, body=body)

    @staticmethod
    def activate_user_link(request: HttpRequest, uidb64: str, token: str) -> None:
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
    def activate_user_token(
        request: HttpRequest, payload: ActivationPayloadType
    ) -> None:
        try:
            obj = PhoneNumberCheck.objects.get(
                token=payload["token"], user__email=payload["email"]
            )
        except User.DoesNotExist:
            obj = None

        if not obj:
            raise TokenError("User not found")

        if not obj.confirm_verification(payload["token"]) and obj.is_expired():
            raise TokenError("Invalid token")

        user = obj.user

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

    @staticmethod
    def request_password_reset_with_link(request: HttpRequest, email: str) -> None:
        domain = get_current_site(request)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            context = {"user": user, "domain": domain, "token": token}
            sendEmail(
                subject=f"Password reset on {domain}",
                context=context,
                to=[user.email],
                template_name="auth/mail/request-rest-password.html",
            )
        return None
    
    @staticmethod
    def request_password_reset_with_token(request: HttpRequest, phone_number: str) -> None:
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            token = PhoneNumberCheck.create_token(user.phone_number)
            body = _(
                "Voici votre code EtablissementMedine: %(token)d. Ne le partager jamais."
            ) % {"token": token}

            sendSMS(to=user.phone_number, body=body)
        
        
    
    @staticmethod
    def request_password_reset_with_token(request: HttpRequest, token: str, phone_number: str):
        try:
            obj = PhoneNumberCheck.objects.get(token=token, user__phone_number=phone_number)
            user = obj.user
        except PhoneNumberCheck.DoesNotExist:
            raise UserNotFoundError("User not found")
        

