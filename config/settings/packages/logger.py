import logging
import logging.config
import os

from config.settings.utils import BASE_DIR, get_env_variable

logger = logging.getLogger(__name__)
LOG_LEVEL = "INFO"
FILE_LOGGER = True if get_env_variable("FILE_LOGGER", "False") == "True" else False
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/logs.log")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        # "special": {
        #     "()": "project.logging.SpecialFilter",
        #     "foo": "bar",
        # },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            # "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            # "filters": ["special"],
        },
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {"level": "INFO", "handlers": ["console"], "propagate": False},
        # "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        # "myproject.custom": {
        #     "handlers": ["console", "mail_admins"],
        #     "level": "INFO",
        #     "filters": ["special"],
        # },
    },
}


if FILE_LOGGER:
    # create log file handler if it doesn't exist
    if not os.path.exists(LOG_FILE_PATH):
        os.mkdir(os.path.join(BASE_DIR, "logs"))

    LOGGING["handlers"].update(
        {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "filename": LOG_FILE_PATH,
            }
        }
    )
    LOGGING["loggers"]["django"]["handlers"] = [
        "mail_admins",
        "console",
        "file",
    ]
    LOGGING["loggers"]["django.request"]["handlers"] = [
        "mail_admins",
        "console",
        "file",
    ]
