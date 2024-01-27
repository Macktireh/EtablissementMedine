from random import randint

from apps.users.types import UserType
from config import settings


def make_token(user: UserType) -> str:
    """
    Generates a token based on the user's ID and the environment.

    Args:
        user (UserType): The user for which to generate the token.

    Returns:
        str: The generated token.
    """
    code = str(randint(100000, 1000000)) if settings.ENV == "production" else "123456"
    return code[:3] + str(user.id)[0] + code[3:]
