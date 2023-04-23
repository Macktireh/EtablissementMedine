from typing import Any

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.auth.api import serializers
from apps.auth.api.drf_schema import (
    signup_responses,
    activation_responses,
    login_responses,
)
from apps.auth.services import AuthService
from apps.base.exceptions import EmailOrPasswordIncorrectError, UserNotVerifiedError
from apps.base.response import succesMsg, failMsg


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.SignupSerializer,
        # operation_description="Create a new user account.",
        responses=signup_responses,
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
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


class ActivationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.ActivationSerializer,
        # operation_description="Activate a user account.",
        operation_id="activation",
        responses=activation_responses,
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        uidb64: str = kwargs.get("uidb64")
        token: str = kwargs.get("token")

        try:
            AuthService.activate_user(request, uidb64, token)
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
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            tokens = AuthService.login(request, email, password)
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
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Requested password reset successfully.",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": succesMsg["THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT"],
                    }
                },
            ),
            status.HTTP_400_BAD_REQUEST: "Validation error.",
        },
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

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
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
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
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        return Response(
            {
                "status": "success",
                "message": succesMsg["LOGOUT_SUCCESS"],
            },
            status=status.HTTP_204_NO_CONTENT,
        )
