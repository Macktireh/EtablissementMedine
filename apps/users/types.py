from typing import TypeVar

from apps.users.models import User

UserType = TypeVar("UserType", bound=User)
