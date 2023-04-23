from collections import OrderedDict

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.auth.models import User
from apps.auth.validators import AuthUserValidators
from apps.base.sender import sendEmail
from apps.base.response import failMsg


class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=128,
        validators=[AuthUserValidators.passwordValidator],
        write_only=True,
        style={"input_type": "password"},
    )
    confirmPassword = serializers.CharField(
        max_length=128, write_only=True, style={"input_type": "password"}
    )


class SignupSerializer(PasswordSerializer):

    name = serializers.CharField(max_length=128)
    phoneNumber = serializers.CharField(
        source="phone_number",
        max_length=24,
        validators=[AuthUserValidators.phoneValidator],
    )
    email = serializers.CharField(validators=[AuthUserValidators.emailValidator])

    class Meta:
        fields = [
            "name",
            "phoneNumber",
            "email",
            "password",
            "confirmPassword",
        ]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get("password")
        confirm_password = attrs.get("confirmPassword")
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirmPassword": failMsg[
                        "THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"
                    ]
                }
            )
        return attrs

    def create(self, validate_data: dict) -> User:
        validate_data.pop("confirmPassword", None)
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})

    class Meta:
        fields = [
            "email",
            "password",
        ]


class RequestResetPasswordSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        request = self.context.get("request")
        domain = get_current_site(request)
        email = attrs.get("email")
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
        return attrs


class ResetPasswordSerializer(PasswordSerializer):
    class Meta:
        fields = ["password", "confirmPassword"]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get("password")
        confirm_password = attrs.get("confirmPassword")
        uid = self.context.get("uid")
        token = self.context.get("token")
        request = self.context.get("request")
        domain = get_current_site(request)

        if password != confirm_password:
            raise serializers.ValidationError(
                failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"]
            )
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(public_id=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(failMsg["USER_DOES_NOT_EXIST"])
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(
                failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"]
            )

        user.set_password(password)
        user.save()
        context = {
            "user": user,
            "domain": domain,
        }

        sendEmail(
            subject=f"{domain} - Votre mot de passe a été changé avec succès !",
            context=context,
            to=[user.email],
            template_name="auth/mail/rest-password-success.html",
        )
        return attrs


class LogoutSerializer(serializers.Serializer):

    public_id = serializers.CharField(write_only=True)
    refresh = serializers.CharField(write_only=True)

    class Meta:
        fields = ["public_id", "refresh"]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        public_id = attrs.get("public_id", None)
        refresh = attrs.get("refresh", None)
        if not public_id or not refresh:
            raise serializers.ValidationError(
                _("Les champs public_id et refresh sont obligatoire.")
            )
        self.public_id = public_id
        self.refresh = refresh
        return attrs

    def save(self, attrs: OrderedDict) -> OrderedDict:
        try:
            RefreshToken(self.refresh).blacklist()
        except TokenError:
            self.fail("refresh_token_invalid")
        try:
            user = User.objects.get(public_id=self.public_id)
            user.last_logout = timezone.now()
            user.save()
            return attrs
        except:
            pass
