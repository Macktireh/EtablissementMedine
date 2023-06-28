from typing import Any, Dict, Tuple

from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.api.serializers import OrderItemSerializer, OrderSerializer
from apps.orders.models import Order
from apps.orders.services import OerderService

# class OrderItemView(viewsets.ReadOnlyModelViewSet):
#     queryset = OrderItem.objects.select_related("user", "product").all()
#     serializer_class = OrderItemSerializer


# class ShoppingCartView(APIView):
#     def post(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
#         """
#         Add to cart a product
#         """
#         productPubliId = kwargs.get("productPubliId")
#         OerderService.add_to_cart(request.user, productPubliId)

#         return Response(
#             {
#                 "status": "success",
#                 "message": "Added to cart",
#             },
#             status=status.HTTP_200_OK,
#         )


# class OrderDetailView(APIView):
#     def patch(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
#         """
#         Update quatity of orderd product
#         """
#         orderPublicId = kwargs.get("orderPublicId")
#         actionQuantity = kwargs.get("actionQuantity")
#         OerderService.update_order(orderPublicId, actionQuantity)

#         return Response(
#             {
#                 "status": "success",
#                 "message": "Updated quantity",
#             },
#             status=status.HTTP_200_OK,
#         )

#     def delete(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
#         """
#         Delete order
#         """
#         orderPublicId = kwargs.get("orderPublicId")
#         OerderService.delete_order(orderPublicId)

#         return Response(
#             {
#                 "status": "success",
#                 "message": "Deleted order",
#             },
#             status=status.HTTP_200_OK,
#         )
