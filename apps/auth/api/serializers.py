from collections import OrderedDict

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.auth.models import User
from apps.base.mail import sendEmail
from apps.base.response import errorMessages, failMsg
from apps.base.validators import emailValidator, passwordValidator, phoneNumverValidator


class SignupSerializer(serializers.ModelSerializer):

    firstName = serializers.CharField(
        source='first_name',
        max_length=150,
        error_messages={
            "blank": errorMessages('blank', 'Prénom'),
            "required": errorMessages('required', 'Prénom'),
        },
    )
    lastName = serializers.CharField(
        source='last_name',
        max_length=150,
        error_messages={
            "blank": errorMessages('blank', 'Nom'),
            "required": errorMessages('required', 'Nom'),
        },
    )
    phoneNumber = serializers.CharField(
        source='phone_number',
        max_length=16,
        validators=[phoneNumverValidator],
        error_messages={
            "blank": errorMessages('blank', 'Numéro de téléphone'),
            "required": errorMessages('required', 'Numéro de téléphone'),
        },
    )
    email = serializers.CharField(
        max_length=255,
        validators=[emailValidator],
        error_messages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )
    password = serializers.CharField(
        max_length=128,
        validators=[passwordValidator], 
        write_only=True, 
        error_messages={
            "blank": errorMessages('blank', 'Mot de passe'),
            "required": errorMessages('required', 'Mot de passe'),
        },
    )
    confirmPassword = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        error_messages={
            "blank": errorMessages('blank', 'Confirmation mot de passe'),
            "required": errorMessages('required', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'phoneNumber', 'email', 'password', 'confirmPassword',]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get('password')
        confirm_password = attrs.get('confirmPassword')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"])
        return attrs

    def create(self, validate_data: dict) -> User:
        validate_data.pop('confirmPassword', None)
        return User.objects.create_user(**validate_data)



class ActivationSerializer(serializers.Serializer):

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['uidb64', 'token',]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        request = self.context.get('request')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        domain = get_current_site(request)

        user, check, send = User.activate_user(uidb64, token)
        
        if user is None or not check:
            raise serializers.ValidationError(failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        
        if send:
            context = {
                'user': user,
                'domain': domain,
            }
            sendEmail(
                subject=f"{domain} - Votre compte a est activer", 
                context=context,
                to=[user.email],
                template_name='auth/mail/activation-success.html', 
            )         
        return attrs



class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        max_length=255,
        error_messages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )
    password = serializers.CharField(
        error_messages={
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
        error_messages={
            "blank": errorMessages('blank', 'email'),
            "required": errorMessages('required', 'email'),
        },
    )

    class Meta:
        fields = ['email']

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        request = self.context.get('request')
        domain = get_current_site(request)
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            context = {
                'user': user,
                'domain': domain,
                'token': token
            }
            sendEmail(
                subject=f"Password reset on {domain}",
                context=context,
                to=[user.email],
                template_name='auth/mail/request-rest-password.html',
            )
        return attrs



class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True, 
        validators=[passwordValidator],
        error_messages={
            "blank": errorMessages('blank', 'Mot de passe'),
            "required": errorMessages('required', 'Mot de passe'),
        },
    )
    confirmPassword = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        error_messages={
            "blank": errorMessages('blank', 'Comfirmation mot de passe'),
            "required": errorMessages('required', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        fields = ['password', 'confirmPassword']

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        password = attrs.get('password')
        confirm_password = attrs.get('confirmPassword')
        uid = self.context.get('uid')
        token = self.context.get('token')
        request = self.context.get('request')
        domain = get_current_site(request)

        if password != confirm_password:
            raise serializers.ValidationError(failMsg["THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH"])
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(public_id=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(failMsg["USER_DOES_NOT_EXIST"])
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(failMsg["THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        
        user.set_password(password)
        user.save()
        context = {
            'user': user,
            'domain': domain,
        }

        sendEmail(
            subject=f"{domain} - Votre mot de passe a été changé avec succès !", 
            context=context,
            to=[user.email],
            template_name='auth/mail/rest-password-success.html', 
        )
        return attrs



class LogoutSerializer(serializers.Serializer):
    
    public_id = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": "Le champ public_id ne doit pas être vide.",
            "required": "Le champ public_id est obligatoire.",
        },
    )
    refresh = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": "Le champ refresh ne doit pas être vide.",
            "required": "Le champ refresh est obligatoire.",
        },
    )
    
    class Meta:
        fields = ['public_id', 'refresh']
        
    def validate(self, attrs: OrderedDict) -> OrderedDict:
        public_id = attrs.get('public_id', None)
        refresh = attrs.get('refresh', None)
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
