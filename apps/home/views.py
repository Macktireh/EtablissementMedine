from typing import Any, Dict, Tuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

class HomeView(View):
    
    template_name = "home/index.html"
    context = {}
    
    def get(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]) -> HttpResponse:
        return render(request, self.template_name, self.context)