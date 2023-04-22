from config.settings.utils import get_env_variable


FILE_LOGGER = True if get_env_variable("FILE_LOGGER", "False") == "True" else False
LOG_FILE_PATH = "logs/logs.log"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
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
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            # "filters": ["special"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        # "myproject.custom": {
        #     "handlers": ["console", "mail_admins"],
        #     "level": "INFO",
        #     "filters": ["special"],
        # },
    },
}


if FILE_LOGGER:
    from pathlib import Path

    p = Path("/var", "/log", "/contaniers")
    p.mkdir(exist_ok=True)

    LOGGING["handlers"].update(
        {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "ecs_formatter",
                "filename": "/var/log/containers/request.log",
            }
        }
    )
    LOGGING["loggers"]["django"]["handlers"] = [
        "console",
        "file",
    ]
    LOGGING["loggers"]["django.request"]["handlers"] = [
        "mail_admins",
        "console",
        "file",
    ]
