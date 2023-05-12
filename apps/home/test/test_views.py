import pytest

from django.test import RequestFactory
from django.urls import reverse

from rest_framework import status

from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestHomeView:

    def setup_method(self) -> None:
        self.factory = RequestFactory()

    def test_home_view_get(self, client) -> None:
        response = client.get(reverse('home:index'))
        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "home/index.html")