from config.settings.utils import get_env_variable

ENV = get_env_variable("ENV", "development")


if ENV == "production":
    from config.settings.production import *  # noqa: F403
elif ENV == "testing":
    from config.settings.testing import *  # noqa: F403
else:
    from config.settings.development import *  # noqa: F403
