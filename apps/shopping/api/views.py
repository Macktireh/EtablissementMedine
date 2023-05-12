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


class CartView(viewsets.ModelViewSet):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['get']



class ShoppingCartView(APIView):

    def post(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        Add to cart a product
        """
        productPubliId = kwargs.get('productPubliId')
        ShoppingService.add_to_cart(request.user, productPubliId)
        
        return Response({
            "status": "success",
            "message": "Added to cart",
        }, status=status.HTTP_200_OK)



class OrderDetailView(APIView):

    def patch(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        Update quatity of orderd product
        """
        orderPublicId = kwargs.get('orderPublicId')
        actionQuantity = kwargs.get('actionQuantity')
        ShoppingService.update_order(orderPublicId, actionQuantity)
        
        return Response({
            "status": "success",
            "message": "Updated quantity",
        }, status=status.HTTP_200_OK)
    
    def delete(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        Delete order
        """
        orderPublicId = kwargs.get('orderPublicId')
        ShoppingService.delete_order(orderPublicId)
        
        return Response({
            "status": "success",
            "message": "Deleted order",
        }, status=status.HTTP_200_OK)
