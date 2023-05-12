from typing import cast

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _

from rest_framework_simplejwt.tokens import RefreshToken, TokenError as JWTTokenError

from apps.auth.models import PhoneNumberCheck, User
from apps.auth.tokens import getTokensUser, tokenGenerator
from apps.auth.types import (
    ActivationLinkPayloadType,
    ActivationTokenPayloadType,
    LoginPayloadType,
    ResetPwdLinkPayloadType,
    ResetPwdTokenPayloadType,
    JWTTokenType,
)
from apps.core.exceptions import (
    EmailOrPasswordIncorrectError,
    TokenError,
    UserNotFoundError,
    UserNotVerifiedError,
)
from apps.core.sender import send_email, send_sms


class AuthService:
    @staticmethod
    def signup_email(request: HttpRequest, user: User) -> None:
        token = tokenGenerator.make_token(user)
        domain = get_current_site(request)
        subject = _("Confirm the email address of your EtablissementMedine account")
        context = {
            "user": user,
            "domain": domain,
            "uidb64": urlsafe_base64_encode(force_bytes(user.public_id)) or None,
            "token": token,
        }
        send_email(
            subject=subject,
            context=context,
            to=[user.email],
            template_name="auth/mail/activation.html",
        )

    @staticmethod
    def signup_sms(request: HttpRequest, user: User) -> None:
        token = PhoneNumberCheck.create_token(user.phone_number)
        body = _(
            "Here is your EtablissementMedine code: %(token)d. Never share it."
        ) % {"token": token}

        send_sms(to=user.phone_number, body=body)

    @staticmethod
    def activate_user_link(
        request: HttpRequest, payload: ActivationLinkPayloadType
    ) -> None:
        try:
            public_id = force_str(urlsafe_base64_decode(payload["uidb64"]))
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            user = None

        if not user:
            raise UserNotFoundError("User not found")

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
                subject=_("%(domain)d - Your account has been successfully activated")
                % {"domain": domain},
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )

    @staticmethod
    def activate_user_token(
        request: HttpRequest, payload: ActivationTokenPayloadType
    ) -> None:
        try:
            obj = PhoneNumberCheck.objects.get(
                token=payload["token"], user__phone_number=payload["phone_number"]
            )
            user = obj.user
        except:
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
                subject=_("%(domain)d - Your account has been successfully activated")
                % {"domain": domain},
                context=context,
                to=[user.email],
                template_name="auth/mail/activation-success.html",
            )

    @staticmethod
    def login(request: HttpRequest, payload: LoginPayloadType) -> JWTTokenType:
        user = cast(
            User,
            authenticate(
                request=request, email=payload["email"], password=payload["password"]
            ),
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
            context = {"user": user, "domain": domain, "token": token}
            send_email(
                subject=f"Password reset on {domain}",
                context=context,
                to=[user.email],
                template_name="auth/mail/request-rest-password.html",
            )
        return None

    @staticmethod
    def request_reset_password_with_token(
        request: HttpRequest, phone_number: str
    ) -> None:
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            token = PhoneNumberCheck.create_token(user.phone_number)
            body = _(
                "Here is your EtablissementMedine code: %(token)d. Never share it."
            ) % {"token": token}

            send_sms(to=user.phone_number, body=body)

    @staticmethod
    def reset_password_with_link(
        request: HttpRequest, payload: ResetPwdLinkPayloadType
    ) -> None:
        try:
            public_id = force_str(urlsafe_base64_decode(payload["uidb64"]))
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            raise UserNotFoundError("User not found")

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
            subject=_("%(domain)d - Your password has been successfully changed!")
            % {"domain": domain},
            context=context,
            to=[user.email],
            template_name="auth/mail/rest-password-success.html",
        )

    @staticmethod
    def reset_password_with_token(
        request: HttpRequest, payload: ResetPwdTokenPayloadType
    ) -> None:
        try:
            obj = PhoneNumberCheck.objects.get(
                token=payload["token"], user__phone_number=payload["phone_number"]
            )
            user = obj.user
        except:
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
            subject=_("%(domain)d - Your password has been successfully changed!")
            % {"domain": domain},
            context=context,
            to=[user.email],
            template_name="auth/mail/rest-password-success.html",
        )

    @staticmethod
    def logout(request: HttpRequest, refresh: str) -> None:
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
        except JWTTokenError:
            raise JWTTokenError("Refresh token is invalid")

        cast(User, request.user).last_login = timezone.now()
        request.user.save()
