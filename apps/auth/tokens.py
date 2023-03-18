import six
from typing import TypedDict

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.tokens import RefreshToken


class TokenType(TypedDict): 
    access: str
    refresh: str


def getTokensUser(user) -> TokenType:
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return (six.text_type(user.public_id) + six.text_type(timestamp) + six.text_type(user.verified))


tokenGenerator = TokenGenerator()
