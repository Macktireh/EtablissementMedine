import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load = load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_env_variable(var_name: str, default: None | str = None, raise_error: bool = True) -> str:
    try:
        if os.environ[var_name]:
            return os.environ[var_name]
        raise KeyError
    except KeyError as e:
        if default is not None:
            return default
        if raise_error:
            raise ImproperlyConfigured(f"Set the {var_name} environment variable") from e
        return ""
