from typing import Any, Dict, Tuple

from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.orders.api.serializers import OrderSerializer
from apps.orders.models import Order


class OrderView(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.select_related("user", "payement").all()
    serializer_class = OrderSerializer

    def list(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
