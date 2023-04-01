from typing import Any

from django.http import HttpRequest

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.shopping.models import Cart
from apps.shopping.api.serializers import CartSerializer
from apps.shopping.services import ShoppingService


class ShoppingCartView(APIView):


    # get all carts
    # @swagger_auto_schema(
    #     request_body=CartSerializer,
    #     operation_description="Get all carts",
    # )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        """
        Get all carts
        """
        user = request.user
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        """
        Add to cart a product
        """
        productPubliId = kwargs.get('productPubliId')
        ShoppingService.add_to_cart(request.user, productPubliId)
        
        return Response({
            "status": "success",
            "message": "Added to cart",
        }, status=status.HTTP_200_OK)


