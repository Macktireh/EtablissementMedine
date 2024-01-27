from typing import Any

from django_components import component


@component.register("cardWarapper")
class CardWarapper(component.Component):
    template_name = "cardWarapper/cardWarapper.html"

    class Media:
        js = "cardWarapper/cardWarapper.js"

    def get_context_data(self, id) -> dict[str, Any]:
        return {"id": id}
