from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status


class HomeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_home_view_get(self) -> None:
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "home/index.html")
