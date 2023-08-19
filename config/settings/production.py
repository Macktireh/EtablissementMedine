from config.settings.base import *  # noqa: F403
from config.settings.packages import *  # noqa: F403
from config.settings.utils import get_env_variable

DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": get_env_variable("DB_ENGINE"),
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
    },
}


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        # "LOCATION": "redis://username:password@127.0.0.1:6379",
        "LOCATION": f"redis://:{get_env_variable('REDIS_PASSWORD')}@{get_env_variable('REDIS_HOST')}:{get_env_variable('REDIS_PORT')}/0",
    }
}


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": get_env_variable("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": get_env_variable("CLOUDINARY_API_KEY"),
    "API_SECRET": get_env_variable("CLOUDINARY_API_SECRET"),
}
