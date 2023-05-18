from typing import Type, TypeVar, TypedDict

from apps.users.models import User


UserType = Type[User]
# UserType = TypeVar("UserType", bound=User)

class CreateTokenPayloadType(TypedDict):
    phone_number: str
    user: UserType