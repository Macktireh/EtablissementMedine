from pprint import pprint
from re import S
from typing import Any, Dict, Mapping, Tuple

from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from render_block import render_block_to_string

from apps.products.models import GroupCategory, Product


def home(request: HttpRequest) -> HttpResponse:
    categories = GroupCategory.objects.all()[:9]
    products = Product.objects.all()
    return render(request, "home/index.html", {"categories": categories, "products": products})


class HomeView(View):
    """
    The HomeView is a class-based view in Django that handles the GET request for rendering the home page.
    It inherits from the View class provided by Django.

    When a GET request is made to the HomeView, the get method is called. Inside the get method,
    it retrieves the first 9 GroupCategory objects and all Product objects from the database.
    It then adds the retrieved objects to the context dictionary.

    Finally, the render function is used to render the home/index.html template
    with the updated context dictionary, and the resulting HTML response is returned.

    In summary, the HomeView is responsible for fetching data from the database, adding it to the context,
    and rendering the home page template with the updated context.

    Inherits from:
        A class that inherits from: `django.views.generic.base.View`


    **Method:**

        :**Get**: A method that retrieves the first 9 GroupCategory objects and all Product objects from the database.

            **Arguments:**

                ``request``: The HTTP request object.

                ``*args``: Variable length argument list.

                ``**kwargs``: Arbitrary keyword arguments.

            **Context:**

                ``products``: An List of instance of :model:`products.Product`.

                ``categories``: An List of instance of :model:`products.GroupCategory`.

            **Template:**

                :template:`home/index.html`
    """

    template_name: str = "home/index.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> HttpResponse:
        categories = GroupCategory.objects.all()[:9]
        products = Product.objects.all()
        self.context["categories"] = categories
        self.context["products"] = products
        return render(request, self.template_name, self.context)


class SearchSuggestionView(View):
    __doc__ = _(
        """
    The SearchSuggestionView is a class-based view  that handles GET requests for searching product suggestions.
    It expects a query parameter named "product" in the request's query string. If the parameter is missing,
    t returns a HttpResponseBadRequest. If the parameter is present,
    it performs a search using the Product model and filters the results based on the search term.
    The search results are added to the view's context dictionary and used to render a specific block of a template.
    Finally, the rendered block is returned as the HTTP response.

    Inherits from:
        django.views.generic.base.View

    **Method:**

        :**Get**: A method that retrieves the first 10 Product objects from the database that match the search query.

            **Arguments:**

                ``request``: The HTTP request object.

                ``*args``: Variable length argument list.

                ``**kwargs``: Arbitrary keyword arguments.

            **Context:**

                ``products``: An List of instance of :model:`products.Product`.

    """
    )

    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> HttpResponse:
        search = request.GET.get("product")
        if not search:
            return HttpResponseBadRequest("search product is required")
        if not request.htmx:
            return HttpResponseBadRequest("only htmx supported")
        search_results = Product.objects.filter(
            Q(name__icontains=search) | Q(slug__icontains=search) | Q(category__name__icontains=search)
        )[:10]
        self.context["search_results"] = search_results
        block = render_block_to_string("searchBar/searchBar.html", "title-product-search", self.context)
        return HttpResponse(block)
