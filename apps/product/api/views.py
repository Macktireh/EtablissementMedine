from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.product.api.serializers import CategorySerializer, ProductSerializer
from apps.product.models import Category, Product


class PermissionMixin:
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "public_id"


class CategoryView(PermissionMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(PermissionMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
