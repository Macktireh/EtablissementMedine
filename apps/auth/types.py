import enum
from typing import TypedDict

from apps.users.types import UserType


class ClientType(str, enum.Enum):
    WEB = "web"
    MOBILE = "mobile"


class JWTTokenType(TypedDict):
    access: str
    refresh: str


class CreateTokenPayloadType(TypedDict):
    phone_number: str
    user: UserType


class ActivationLinkPayloadType(TypedDict):
    uidb64: str
    token: str


class ActivationTokenPayloadType(TypedDict):
    token: str
    phone_number: str


class LoginPayloadType(TypedDict):
    email: str
    password: str


class ResetPwdLinkPayloadType(ActivationLinkPayloadType):
    password: str


class ResetPwdTokenPayloadType(ActivationTokenPayloadType):
    password: str
