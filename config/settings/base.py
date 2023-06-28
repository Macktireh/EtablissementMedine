import os

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

from config.settings.utils import BASE_DIR, get_env_variable

DEFAULT_SECRET_KEY = get_random_secret_key() + get_random_secret_key() + get_random_secret_key()
SECRET_KEY = get_env_variable("SECRET_KEY", DEFAULT_SECRET_KEY)

ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS", "127.0.0.1 localhost 10.0.2.2").split(" ")

ADMINS = [tuple(map(str.strip, i.split("/"))) for i in get_env_variable("ADMINS", "").split("%%")]


# Application definition
THIRD_PARTY_APPS_BEFORE_DJANGO_APPS = [
    "modeltranslation",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.home.apps.HomeConfig",
    "apps.users.apps.UsersConfig",
    "apps.auth.apps.AuthUserConfig",
    "apps.products.apps.ProductsConfig",
    "apps.cart.apps.CartConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.payments.apps.PaymentsConfig",
]

INSTALLED_APPS = THIRD_PARTY_APPS_BEFORE_DJANGO_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Locale Middleware
    "corsheaders.middleware.CorsMiddleware",  # CORS Middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",  # django admin docs middleware
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
)

prefix_default_language = False

LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

MODELTRANSLATION_LANGUAGES = ("en", "fr")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en",)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"


# Email settings
EMAIL_HOST = get_env_variable("EMAIL_HOST", raise_error=False)
EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER", raise_error=False)
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD", raise_error=False)
EMAIL_PORT = get_env_variable("EMAIL_PORT", raise_error=False)
EMAIL_USE_TLS = get_env_variable("EMAIL_USE_TLS", raise_error=False)
DEFAULT_FROM_EMAIL = get_env_variable("EMAIL_HOST_USER", raise_error=False)
SERVER_EMAIL = get_env_variable("EMAIL_HOST_USER", raise_error=False)

# SMS
PHONENUMBER_EXPIRATION = 5
CLICKSEND_URL = "https://rest.clicksend.com/v3/sms/send"
CLICKSEND_USERNAME = get_env_variable("CLICKSEND_USERNAME", raise_error=False)
CLICKSEND_PASSWORD = get_env_variable("CLICKSEND_PASSWORD", raise_error=False)
CLICKSEND_FROM = "EtabMedine"


# the list of origins authorized to make HTTP requests
CORS_ALLOWED_ORIGINS = get_env_variable("CORS_ALLOWED_ORIGINS", raise_error=False).split(" ")

DOMAIN_FRONTEND = get_env_variable("DOMAIN_FRONTEND", raise_error=False)


GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}


DJANGORESIZED_DEFAULT_SIZE = [400, 400]
DJANGORESIZED_DEFAULT_QUALITY = 90
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
