from typing import Any

from django_components import component

from apps.products.models import Category


@component.register("searchBar")
class SearchBar(component.Component):
    template_name = "searchBar/searchBar.html"

    class Media:
        js = "searchBar/searchBar.js"

    def get_context_data(self) -> dict[str, Any]:
        categories = Category.objects.all()
        return {"categories": categories}
