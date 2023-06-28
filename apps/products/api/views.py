from typing import Any, Dict, Tuple

from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.products.api.serializers import CategorySerializer, ProductSerializer
from apps.products.models import Category, Product


class PermissionMixin:
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "public_id"


class CategoryListView(PermissionMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(PermissionMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

    def list(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
