from config.settings.utils import get_env_variable


ENV = get_env_variable("ENV", "development")


if ENV == "production":
    from config.settings.production import *
elif ENV == "testing":
    from config.settings.testing import *
else:
    from config.settings.development import *
