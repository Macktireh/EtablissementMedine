from django.test import TestCase, RequestFactory


class HomeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_home_view_get(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
