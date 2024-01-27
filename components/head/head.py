from typing import Any

from django_components import component


@component.register("head")
class Head(component.Component):
    template_name = "head/head.html"

    class Media:
        js = "head/head.js"

    def get_context_data(self) -> dict[str, Any]:
        return {}
