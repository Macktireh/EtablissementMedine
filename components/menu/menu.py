from typing import Any

from django_components import component


@component.register("menu")
class Menu(component.Component):
    template_name = "menu/menu.html"

    def get_context_data(self) -> dict[str, Any]:
        return {}

    class Media:
        js = "menu/menu.js"
