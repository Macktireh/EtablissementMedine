import os

from django.core.exceptions import ImproperlyConfigured

from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load = load_dotenv(os.path.join(BASE_DIR, '.env'))


def get_env_variable(var_name: str, default: None | str = None) -> str:
    try:
        if os.environ[var_name]:
            return os.environ[var_name]
        raise KeyError
    except KeyError:
        if default is not None:
            return default
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)
