from typing import Any

from django_components import component


@component.register("menu")
class Menu(component.Component):
    template_name = "menu/menu.html"

    class Media:
        js = "menu/menu.js"

    def get_context_data(self) -> dict[str, Any]:
        return {}
