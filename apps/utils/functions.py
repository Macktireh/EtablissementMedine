

from uuid import uuid4


def uidGenerator() -> str:
    return str(uuid4()).replace('-', '') + str(uuid4()).replace('-', '')
