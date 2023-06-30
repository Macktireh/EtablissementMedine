import mimetypes
import os
import socket

from config.settings.base import *  # noqa: F403
from config.settings.packages import *  # noqa: F403
from config.settings.utils import BASE_DIR

DEBUG = True

INSTALLED_APPS.extend(["django_extensions", "debug_toolbar", "rosetta"])  # noqa: F405
MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])  # noqa: F405


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    # "default": {
    #     "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379",
    # }
}


MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Django-debug-toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]
mimetypes.add_type("application/javascript", ".js", True)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "INSERT_BEFORE": "</head>",
    "RENDER_PANELS": True,
}
