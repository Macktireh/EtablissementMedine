from typing import Any, Dict, Mapping, Tuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):

    template_name: str = "home/index.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> HttpResponse:
        return render(request, self.template_name, self.context)