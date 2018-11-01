from django.urls import include, path

from api.views import AnimeListView


urlpatterns = [
    path('v1/animes/', AnimeListView.as_view()),
]
