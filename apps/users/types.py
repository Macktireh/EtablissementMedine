from typing import TypedDict, TypeVar

from apps.users.models import User

UserType = TypeVar("UserType", bound=User)


class CreateTokenPayloadType(TypedDict):
    phone_number: str
    user: UserType
