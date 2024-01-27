from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status


class HomeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_home_view_get(self) -> None:
        # Send a GET request to the URL specified by the reverse function, which resolves to the "home:index" path
        response = self.client.get(reverse("home:index"))

        # Assert that the status code of the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response rendered the "home/index.html" template
        self.assertTemplateUsed(response, "home/index.html")


# class HomeViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.view = HomeView.as_view()
#         self.template_name = "home/index.html"
#         self.category = Category.objects.create(name="Category 1")
#         self.product = Product.objects.create(name="Product 1")

#     def test_home_view(self):
#         # Create some test data

#         # Set up the request
#         url = reverse("home:index")
#         request = self.factory.get(url)

#         # Call the view
#         response = self.view(request)

#         # Check that the response is successful
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         # self.assertTemplateUsed(response, self.template_name)

#         # Check that the context contains the expected data
#         self.assertContains(response, self.category.name)
#         self.assertContains(response, self.product.name)


# class SearchPartialViewTestCase(TestCase):
#     def test_get_with_valid_search(self):
#         view = SearchPartialView()

#         # Mock the request object
#         request = MagicMock(spec=HttpRequest)
#         request.GET.get.return_value = "valid_search"
#         request.htmx = True

#         # Call the get method
#         response = view.get(request)

#         # Assert the response
#         self.assertIsInstance(response, HttpResponse)
#         # Add more assertions as needed

#     def test_get_with_invalid_search(self):
#         view = SearchPartialView()

#         # Mock the request object
#         request = MagicMock(spec=HttpRequest)
#         request.GET.get.return_value = None
#         request.htmx = True

#         # Call the get method
#         response = view.get(request)

#         # Assert the response
#         self.assertIsInstance(response, HttpResponseBadRequest)
#         # Add more assertions as needed

#     def test_get_with_htmx_not_supported(self):
#         view = SearchPartialView()

#         # Mock the request object
#         request = MagicMock(spec=HttpRequest)
#         request.GET.get.return_value = "valid_search"
#         request.htmx = False

#         # Call the get method
#         response = view.get(request)

#         # Assert the response
#         self.assertIsInstance(response, HttpResponseBadRequest)
#         # Add more assertions as needed

#     def test_get_with_search_results(self):
#         view = SearchPartialView()

#         # Mock the request object
#         request = MagicMock(spec=HttpRequest)
#         request.GET.get.return_value = "valid_search"
#         request.htmx = True

#         # Mock the Product.objects.filter method to return search results
#         search_results = [Product(name="Product 1"), Product(name="Product 2")]
#         Product.objects.filter.return_value = search_results

#         # Call the get method
#         response = view.get(request)

#         # Assert the response
#         self.assertIsInstance(response, HttpResponse)
