from typing import cast

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _

from apps.auth.models import CodeChecker
from apps.auth.tokens import getTokensUser, tokenGenerator
from apps.auth.types import (
    ActivationLinkPayloadType,
    ActivationTokenPayloadType,
    ClientType,
    CreateTokenPayloadType,
    JWTTokenType,
    LoginPayloadType,
    ResetPwdLinkPayloadType,
    ResetPwdTokenPayloadType,
)
from apps.core.exceptions import EmailOrPasswordIncorrectError, NotFound, TokenError, UserNotVerifiedError
from apps.core.sender import send_email, send_sms
from apps.users.types import UserType

User = cast(UserType, get_user_model())


class AuthService:
    @staticmethod
    def signup_email(request: HttpRequest, user: UserType, client: ClientType = ClientType.WEB) -> None:
        if client == ClientType.MOBILE:
            payload = CreateTokenPayloadType(phone_number=user.phone_number, user=user)
            token = CodeChecker.create_token(payload)
            template_name = "auth/mail/activation_code.html"
        else:
            token = tokenGenerator.make_token(user)
            template_name = "auth/mail/activation_link.html"
        domain = get_current_site(request)
        subject = _("Account Activation") + " - EtablissementMedine"
        context = {
            "user": user,
            "domain": domain,
            "uidb64": urlsafe_base64_encode(force_bytes(user.public_id)),
            "token": token,
        }
        send_email(
            subject=subject,
            context=context,
            to=[user.email],
            template_name=template_name,
        )

    @staticmethod
    def signup_sms_code(request: HttpRequest, user: UserType) -> None:
        payload = CreateTokenPayloadType(phone_number=user.phone_number, user=user)
        token = CodeChecker.create_token(payload)
        body = _("Here is your EtablissementMedine code: %(token)s. Never share it.") % {"token": token}

        send_sms(body=body, to=user.phone_number)

    @staticmethod
    def activate_user_link(request: HttpRequest, payload: ActivationLinkPayloadType) -> None:
        try:
            public_id = force_str(urlsafe_base64_decode(payload["uidb64"]))
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

        if not tokenGenerator.check_token(user, payload["token"]):
            raise TokenError("Invalid token")

        if not user.verified:
            user.verified = True
            user.save()
            domain = get_current_site(request)
            context = {
                "user": user,
                "domain": domain,
            }
            send_email(
                subject=_("Account Activation Successful") + " - EtablissementMedine",
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )

    @staticmethod
    def activate_user_token(request: HttpRequest, payload: ActivationTokenPayloadType) -> None:
        try:
            obj = CodeChecker.objects.get(token=payload["token"], user__phone_number=payload["phone_number"])
            user = obj.user
        except CodeChecker.DoesNotExist:
            raise TokenError("User not found")

        if not obj.confirm_verification(payload["token"]) and obj.is_expired():
            raise TokenError("Invalid token")

        if not user.verified:
            user.verified = True
            user.save()
            domain = get_current_site(request)
            context = {
                "user": user,
                "domain": domain,
            }
            send_email(
                subject=_("Account Activation Successful") + " - EtablissementMedine",
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )

    @staticmethod
    def login(request: HttpRequest, payload: LoginPayloadType) -> JWTTokenType:
        user = cast(
            UserType,
            authenticate(request=request, email=payload["email"], password=payload["password"]),
        )

        if not user:
            raise EmailOrPasswordIncorrectError("Email or password incorrect")

        if not user.verified:
            raise UserNotVerifiedError("User not verified")

        user.last_login = timezone.now()
        user.save()
        return getTokensUser(user)

    @staticmethod
    def request_reset_password_with_link(request: HttpRequest, email: str) -> None:
        domain = get_current_site(request)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            context = {
                "user": user,
                "domain": domain,
                "uidb64": urlsafe_base64_encode(force_bytes(user.public_id)),
                "token": token,
            }
            send_email(
                subject=_("Password Reset") + " - EtablissementMedine",
                context=context,
                to=[user.email],
                template_name="auth/mail/request-rest-password.html",
            )
        return None

    @staticmethod
    def request_reset_password_with_token(request: HttpRequest, phone_number: str) -> None:
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            token = CodeChecker.create_token(user.phone_number)
            body = _("Here is your EtablissementMedine code: %(token)s. Never share it.") % {"token": token}

            send_sms(body=body, to=user.phone_number)

    @staticmethod
    def reset_password_with_link(request: HttpRequest, payload: ResetPwdLinkPayloadType) -> None:
        try:
            public_id = force_str(urlsafe_base64_decode(payload["uidb64"]))
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            raise TokenError("Invalid token")

        if not PasswordResetTokenGenerator().check_token(user, payload["token"]):
            raise TokenError("Invalid token")

        user.set_password(payload["password"])
        user.save()
        domain = get_current_site(request)
        context = {
            "user": user,
            "domain": domain,
        }
        send_email(
            subject=_("Password reset success") + " - EtablissementMedine",
            context=context,
            to=[user.email],
            template_name="auth/mail/rest-password-success.html",
        )

    @staticmethod
    def reset_password_with_token(request: HttpRequest, payload: ResetPwdTokenPayloadType) -> None:
        try:
            obj = CodeChecker.objects.get(token=payload["token"], user__phone_number=payload["phone_number"])
            user = obj.user
        except CodeChecker.DoesNotExist:
            raise TabError("Invalid token")

        if not obj.confirm_verification(payload["token"]) and obj.is_expired():
            raise TokenError("Invalid token")

        user.set_password(payload["password"])
        user.save()
        domain = get_current_site(request)
        context = {
            "user": user,
            "domain": domain,
        }
        send_email(
            subject=_("Password reset success") + " - EtablissementMedine",
            context=context,
            to=[user.email],
            template_name="auth/mail/rest-password-success.html",
        )
