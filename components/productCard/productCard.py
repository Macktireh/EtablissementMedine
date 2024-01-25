from typing import Any

from django_components import component


@component.register("productCard")
class ProductCard(component.Component):
    template_name = "productCard/productCard.html"

    def get_context_data(self, product) -> dict[str, Any]:
        return {"product": product}
