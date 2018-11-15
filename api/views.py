from rest_framework import generics

from api.models import Anime
from api.serializers import AnimeSerializer

# Create your views here.


class AnimeListView(generics.ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeDetailView(generics.RetrieveAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
