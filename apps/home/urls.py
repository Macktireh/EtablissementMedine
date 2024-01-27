from django.urls import path

from apps.home.views import HomeView, SearchSuggestionView

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("products/search/", SearchSuggestionView.as_view(), name="search"),
]
