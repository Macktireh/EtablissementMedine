from django.urls import include, path

from apps.core.swagger import schema_view

routes_v1 = [
    path("v1/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-redoc"),
    path("v1/auth/user/", include("apps.auth.api.urls")),
    path("v1/user/", include("apps.users.api.urls")),
    path("v1/products/", include("apps.products.api.urls")),
    path("v1/cart/", include("apps.cart.api.urls")),
    path("v1/orders/", include("apps.orders.api.urls")),
]


urlpatterns = routes_v1
