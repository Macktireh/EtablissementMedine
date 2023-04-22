
from config.settings.base import *
from config.settings.packages import *


DEBUG = True

INSTALLED_APPS.extend(["django_extensions"])


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    # "default": {
    #     "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379",
    # }
}


MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles/')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


