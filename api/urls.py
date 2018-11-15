from django.urls import include, path

from api.views import AnimeDetailView, AnimeListView


urlpatterns = [
    path('v1/animes/', AnimeListView.as_view()),
    path('v1/animes/<int:pk>/', AnimeDetailView.as_view()),
    path('auth/', include('rest_framework.urls')),
]
