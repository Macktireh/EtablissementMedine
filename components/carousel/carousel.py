from typing import Any

from django_components import component

from apps.products.models import ProductAdvertising


@component.register("carousel")
class Carousel(component.Component):
    template_name = "carousel/carousel.html"

    def get_context_data(self) -> dict[str, Any]:
        categories = ProductAdvertising.objects.all()
        return {"categories": categories}

    class Media:
        js = "carousel/carousel.js"
