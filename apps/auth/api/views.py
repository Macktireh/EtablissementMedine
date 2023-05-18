from typing import Any, cast

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.auth.api import serializers
from apps.auth.api.drf_schema import (
    signup_responses,
    activation_responses,
    login_responses,
    request_reset_passwoard_responses,
)
from apps.auth.services import AuthService
from apps.auth.types import (
    ActivationLinkPayloadType,
    ActivationTokenPayloadType,
    LoginPayloadType,
)
from apps.core.exceptions import EmailOrPasswordIncorrectError, UserNotVerifiedError
from apps.core.response import succesMsg, failMsg


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.SignupSerializer,
        operation_description="Create a new user account.",
        responses=signup_responses,
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # AuthService.signup_email(request, user)
        AuthService.signup_sms(request, user)

        return Response(
            {
                "status": "success",
                "message": succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_REGISTERED"],
            },
            status=status.HTTP_201_CREATED,
        )


class ActivationWithLinkView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="activation_with_link",
        responses=activation_responses,
    )
    def get(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        if not uidb64 or not token:
            return Response(
                {
                    "status": _("fail"),
                    "message": failMsg["MISSING_PARAMETER"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = ActivationLinkPayloadType(uidb64=uidb64, token=token)

        try:
            AuthService.activate_user_link(request, payload)
        except:
            return Response(
                {
                    "status": _("fail"),
                    "message": failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "status": "success",
                "message": succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED"],
            },
            status=status.HTTP_200_OK,
        )


class ActivationWithTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.ActivationTokenSerializer,
        operation_id="activation_with_token",
        responses=activation_responses,
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        serializer = serializers.ActivationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = cast(ReturnDict, serializer.validated_data)["token"]
        phone_number = cast(ReturnDict, serializer.validated_data)["phoneNumber"]
        payload = ActivationTokenPayloadType(token=token, phone_number=phone_number)

        try:
            AuthService.activate_user_token(request, payload)
        except:
            return Response(
                {
                    "status": _("fail"),
                    "message": failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "status": "success",
                "message": succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED"],
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.LoginSerializer,
        # operation_description="Endpoint pour l'authentification d'un utilisateur.",
        operation_id="login",
        responses=login_responses,
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = cast(ReturnDict, serializer.validated_data)["email"]
        password = cast(ReturnDict, serializer.validated_data)["password"]
        payload = LoginPayloadType(email=email, password=password)

        try:
            tokens = AuthService.login(request, payload)
        except EmailOrPasswordIncorrectError:
            return Response(
                {
                    "status": _("fail"),
                    "message": failMsg["THE_EMAIL_OR_PASSWORD_IS_INCORRECT"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserNotVerifiedError:
            return Response(
                {
                    "status": _("fail"),
                    "message": failMsg["PLEASE_CONFIRM_YOUR_ADDRESS_EMAIL"],
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "status": "success",
                "message": succesMsg["LOGIN_SUCCESS"],
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class RequestResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.RequestResetPasswordSerializer,
        operation_description="Request a password reset.",
        operation_id="request_reset_password",
        responses=request_reset_passwoard_responses,
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        serializer = serializers.RequestResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = cast(ReturnDict, serializer.validated_data)["email"]
        AuthService.request_reset_password_with_link(request, email)

        return Response(
            {
                "status": "success",
                "message": succesMsg["THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT"],
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.ResetPasswordSerializer,
        operation_description="Reset a password.",
        operation_id="reset_password",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Password reset successfully.",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": succesMsg[
                            "THE_PASSWORD_HAS_BEEN_CHANGED_SUCCESSFULLY"
                        ],
                    }
                },
            ),
            status.HTTP_400_BAD_REQUEST: "Validation error.",
        },
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        serializer = serializers.ResetPasswordSerializer(
            data=request.data, context={"uid": uidb64, "token": token}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "status": "success",
                "message": succesMsg["THE_PASSWORD_HAS_BEEN_CHANGED_SUCCESSFULLY"],
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    @swagger_auto_schema(
        request_body=serializers.ResetPasswordSerializer,
        operation_description="Reset a password.",
        operation_id="reset_password",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Successfully logged out.",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": succesMsg["LOGOUT_SUCCESS"],
                    }
                },
            ),
        },
    )
    def post(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        return Response(
            {
                "status": "success",
                "message": succesMsg["LOGOUT_SUCCESS"],
            },
            status=status.HTTP_204_NO_CONTENT,
        )
