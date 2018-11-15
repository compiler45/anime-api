from django.urls import include, path

from api.views import (AnimeDetailView, AnimeListView, CharacterDetailView,
                       CharacterListView)


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('v1/animes/', AnimeListView.as_view()),
    path('v1/animes/<int:pk>/', AnimeDetailView.as_view()),
    path('v1/characters/', CharacterListView.as_view()),
    path('v1/characters/<int:pk>/', CharacterDetailView.as_view()),
]
