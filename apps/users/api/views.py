from typing import Any

from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import UserSerializer


class CurrentUserView(APIView):
    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
