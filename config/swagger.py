from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
   openapi.Info(
      title="Etablissement Medine API",
      default_version='v1',
      description="This is the Full Rest Json API part of the Etablissement Medine",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mack.abdisoubaneh@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)
