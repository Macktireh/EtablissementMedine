from typing import TypedDict


class TokenType(TypedDict):
    access: str
    refresh: str


class ActivationPayloadType(TypedDict):
    token: str
    email: str
