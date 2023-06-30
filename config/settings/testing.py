from config.settings.base import *  # noqa: F403
from config.settings.packages import *  # noqa: F403
from config.settings.utils import BASE_DIR, get_env_variable

DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# STORAGES = {
#     "default": {
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": get_env_variable("CLOUDINARY_CLOUD_NAME", raise_error=False),
    "API_KEY": get_env_variable("CLOUDINARY_API_KEY", raise_error=False),
    "API_SECRET": get_env_variable("CLOUDINARY_API_SECRET", raise_error=False),
}
