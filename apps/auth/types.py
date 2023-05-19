from typing import TypedDict


class JWTTokenType(TypedDict):
    access: str
    refresh: str


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
