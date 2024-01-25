from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns = [
    *i18n_patterns(path("", include("config.urls.web"))),
    path("api/", include("config.urls.api")),
]


if settings.DEBUG:
    # import debug_toolbar
    from django.conf.urls.static import static

    # urlpatterns.append(path("__debug__", include(debug_toolbar.urls)))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(i18n_patterns(path("rosetta/", include("rosetta.urls"))))
    urlpatterns.append(path("emails/", include("developmentEmailDashboard.urls")))
