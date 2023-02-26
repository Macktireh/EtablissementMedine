from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.tokens import tokenGenerator
from apps.utils.email import sendEmail
from apps.utils.response import errorMessages, failMsg
from apps.utils.validators import emailValidator, passwordValidator


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    firstName = serializers.CharField(
        source='first_name', 
        errorMessages={
            "blank": errorMessages('blank', 'Prénom'),
            "required": errorMessages('required', 'Prénom'),
        },
    )
    lastName = serializers.CharField(
        source='last_name', 
        errorMessages={
            "blank": errorMessages('blank', 'Nom'),
            "required": errorMessages('required', 'Nom'),
        },
    )
    phoneNumber = serializers.CharField(
        source='phone_number', 
        errorMessages={
            "blank": errorMessages('blank', 'Numéro de téléphone'),
            "required": errorMessages('required', 'Numéro de téléphone'),
        },
    )
    email = serializers.CharField(
        validators=[emailValidator],
        errorMessages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )
    password = serializers.CharField(
        validators=[passwordValidator], 
        write_only=True, 
        errorMessages={
            "blank": errorMessages('blank', 'Mot de passe'),
            "required": errorMessages('required', 'Mot de passe'),
        },
    )
    confirmPassword = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        errorMessages={
            "blank": errorMessages('blank', 'Confirmation mot de passe'),
            "required": errorMessages('required', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'phoneNumber', 'email', 'password', 'confirmPassword',]

    def validate(self, attrs) -> Any:
        password = attrs.get('password')
        confirm_password = attrs.get('confirmPassword')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"])
        return attrs

    def create(self, validate_data):
        validate_data.pop('confirmPassword', None)
        return User.objects.create_user(**validate_data)


class ActivationAccountSerializer(serializers.Serializer):

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['uidb64', 'token',]

    def validate(self, attrs):
        request = self.context.get('request', None)
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(public_id=uid)
        except Exception as e:
            user = None
        if user and tokenGenerator().check_token(user, token):
            if not user.is_verified_email:
                user.is_verified_email = True
                user.save()
                context = {
                    'user': user,
                    'domain': get_current_site(request),
                    # 'uid': urlsafe_base64_encode(force_bytes(user.public_id)) or None,
                    # 'token': token
                }
                sendEmail(
                    subject=f"{settings.DOMAIN_FRONTEND} - Your account has been successfully created and activated!", 
                    context=context,
                    to=[user.email],
                    template_name='authentication/mail/activate_success.html', 
                )
        else:
            raise serializers.ValidationError(failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        return attrs


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        max_length=255,
        errorMessages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )
    password = serializers.CharField(
        errorMessages={
            "blank": errorMessages('blank', 'Mot de passe'),
            "required": errorMessages('required', 'Mot de passe'),
        },
    )

    class Meta:
        model = User
        fields = ['email', 'password',]


class RequestResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        max_length=255,
        errorMessages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        current_site = self.context.get('current_site')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            sendEmail(
                subject=f"Réinitialisation du mot de passe sur {current_site}",
                template_name='authentication/mail/send_email_reset_password.html',
                user=user,
                token=token,
                domain=settings.DOMAIN_FRONTEND
            )
        # else:
        #     raise serializers.ValidationError(failMsg["THE_EMAIL_ADDRESS_DOES_NOT_EXIST"])
        return attrs


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True, 
        validators=[passwordValidator],
        errorMessages={
            "blank": errorMessages('blank', 'Mot de passe'),
            "required": errorMessages('required', 'Mot de passe'),
        },
    )
    confirm_password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        errorMessages={
            "blank": errorMessages('blank', 'Comfirmation mot de passe'),
            "required": errorMessages('required', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != confirm_password:
            raise serializers.ValidationError(failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"])
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(public_id=uid)
        except Exception as e:
            user = None
        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            sendEmail(
                subject=f"{settings.DOMAIN_FRONTEND} - Votre mot de passe a été changé avec succès !", 
                template_name='authentication/mail/password_rest_success.html', 
                user=user, 
                domain=settings.DOMAIN_FRONTEND
            )
        else:
            raise serializers.ValidationError(failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        return attrs


class LogoutSerializer(serializers.Serializer):
    
    public_id = serializers.CharField(
        write_only=True,
        errorMessages={
            "blank": "Le champ public_id ne doit pas être vide.",
            "required": "Le champ public_id est obligatoire.",
        },
    )
    refresh = serializers.CharField(
        write_only=True,
        errorMessages={
            "blank": "Le champ refresh ne doit pas être vide.",
            "required": "Le champ refresh est obligatoire.",
        },
    )
    
    class Meta:
        fields = ['public_id', 'refresh']
        
    def validate(self, attrs):
        public_id = attrs.get('public_id', None)
        refresh = attrs.get('refresh', None)
        if not public_id or not refresh:
            raise serializers.ValidationError(
                _("Les champs public_id et refresh sont obligatoire.")
            )
        self.public_id = public_id
        self.refresh = refresh
        return attrs
    
    def save(self, attrs):
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