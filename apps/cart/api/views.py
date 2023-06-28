from typing import Any, Dict, Tuple

from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api import serializers
from apps.cart.api.drf_schema import add_to_cart_responses
from apps.cart.models import OrderItem
from apps.cart.services import CartService


class CartListView(viewsets.ReadOnlyModelViewSet):
    queryset = OrderItem.objects.select_related("user", "product").all()
    serializer_class = serializers.OrderItemSerializer

    def list(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        """
        Handle GET request to list the cart items.

        Args:
            request (HttpRequest): The incoming request.
            *args (Tuple[Any, ...]): Variable length argument list.
            **kwargs (Dict[str, Any]): Arbitrary keyword arguments.

        Returns:
            Response: The serialized data of the queryset.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    @swagger_auto_schema(
        request_body=serializers.AddToCartSerializer,
        responses=add_to_cart_responses,
    )
    def post(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        """
        Handle POST request to add a product to the cart.

        Args:
            request (HttpRequest): The HTTP request object.
            args (Tuple): Positional arguments.
            kwargs (Dict): Keyword arguments.

        Returns:
            Response: The HTTP response with the status and message.
        """
        serializer = serializers.AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CartService.add_to_cart(
            request=request, product_public_id=serializer.validated_data["productPublicId"]
        )

        return Response(
            {
                "status": "success",
                "message": "Added to cart",
            },
            status=status.HTTP_200_OK,
        )


class UpdateOrderItemQuantityView(APIView):
    def post(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        """
        Handle POST request to update order item quantity.

        Args:
            request (HttpRequest): The HTTP request object.
            *args (Tuple[Any, ...]): Variable length argument list.
            **kwargs (Dict[str, Any]): Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.
        """
        # Create serializer instance
        serializer = serializers.UpdateOrderItemQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CartService.update_order_item_quantity(
            order_item_public_id=serializer.validated_data["orderItemPublicId"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {
                "status": "success",
                "message": "Updated quantity",
            },
            status=status.HTTP_200_OK,
        )


class ClearCartView(APIView):
    def delete(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Response:
        """
        Handle DELETE request to clear the cart

        Args:
            request (HttpRequest): The HTTP request object.
            args (Tuple): Positional arguments.
            kwargs (Dict): Keyword arguments.

        Returns:
            Response: The HTTP response with the status and message.
        """
        CartService.clear_cart(request)

        return Response(
            {
                "status": "success",
                "message": "Cart cleared",
            },
            status=status.HTTP_200_OK,
        )
