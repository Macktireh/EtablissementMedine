from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):

    template_name: str = "home/index.html"
    context: Mapping[str, Any] = {}

    def get(self, request: HttpRequest ,*args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, self.context)
