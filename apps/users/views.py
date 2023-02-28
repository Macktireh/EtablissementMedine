from typing import Any

from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _

from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.users import serializers
from apps.users.tokens import tokenGenerator, getTokensUser
from apps.utils.email import sendEmail
from apps.utils.response import succesMsg, failMsg


User = get_user_model()


class SignupView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.SignupSerializer
    http_method_names = ['post']

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = tokenGenerator.make_token(user)
            domain = get_current_site(request)
            subject = f"Activation du compte sur {domain}"
            context = {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.public_id)) or None,
                'token': token
            }
            sendEmail(subject=subject, context=context, to=[user.email], template_name="users/mail/activate.html")
            return Response(
                {
                    "status": "success",
                    'message': succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_REGISTERED"]
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ActivationView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.ActivationSerializer
    http_method_names = ['post']

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    "status": "success",
                    'message': succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED"]
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.LoginSerializer
    http_method_names = ['post']

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    user.last_login = timezone.now()
                    user.save()
                    tokens = getTokensUser(user)
                    return Response(
                        {
                            "status": "success",
                            'message': succesMsg["LOGIN_SUCCESS"], 
                            "tokens": tokens
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "status": "fail",
                            'message': failMsg["PLEASE_CONFIRM_YOUR_ADDRESS_EMAIL"], 
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        "status": "fail",
                        'message': failMsg["THE_EMAIL_OR_PASSWORD_IS_INCORRECT"], 
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestResetPasswordView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.RequestResetPasswordSerializer
    http_method_names = ['post']

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    "status": "success",
                    'message': succesMsg["THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT"], 
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.ResetPasswordSerializer
    http_method_names = ['post']

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        serializer = serializers.UserResetPasswordSerializer(data=request.data, context={'uid': uidb64, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    "status": "success",
                    'message': succesMsg["THE_PASSWORD_HAS_BEEN_CHANGED_SUCCESSFULLY"], 
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = serializers.LogoutSerializer
    http_method_names = ['post']
    lookup_field = 'public_id'

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = serializers.LogoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    "status": "success",
                    'message': succesMsg["LOGOUT_SUCCESS"], 
                }, 
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
