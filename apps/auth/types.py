from enum import Enum
from typing import TypedDict


class ClientType(str, Enum):
    WEB = "web"
    MOBILE = "mobile"


class JWTTokenType(TypedDict):
    access: str
    refresh: str


class ActivationLinkPayloadType(TypedDict):
    uidb64: str
    token: str


class ActivationPayloadToken(TypedDict):
    email: str
    token: str


class LoginPayload(TypedDict):
    email: str
    password: str


class ResetPwdLinkPayloadType(ActivationLinkPayloadType):
    password: str


class ResetPwdTokenPayloadType(ActivationPayloadToken):
    pass
