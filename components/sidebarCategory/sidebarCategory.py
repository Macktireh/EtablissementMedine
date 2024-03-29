from typing import Any

from django_components import component


@component.register("sidebarCategory")
class SidebarCategory(component.Component):
    template_name = "sidebarCategory/sidebarCategory.html"

    def get_context_data(self, categories) -> dict[str, Any]:
        return {"categories": categories}
