from typing import Any, Dict, List, Mapping, Tuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.products.models import Product


class ProductView(View):
    template_name: str = "products/list.html"
    context: Mapping[str, Any] = {}

    def get_context(self) -> Mapping[str, Any]:
        return self.context

    def get(self, request: HttpRequest, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> HttpResponse:
        product_search = request.GET.get("product")
        cagetory_search = request.GET.get("category")
        products: List[Product]

        if not product_search and (cagetory_search == "all" or not cagetory_search):
            products = Product.objects.select_related("category").all()
        else:
            products = Product.objects.select_related("category").filter(
                name__icontains=product_search, category__name__icontains=cagetory_search
            )
        self.context["products"] = products
        return render(request, self.template_name, self.context)
