from rest_framework import generics

from api.models import Anime, Character
from api.serializers import AnimeSerializer, CharacterSerializer

# Create your views here.


class AnimeListView(generics.ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class AnimeDetailView(generics.RetrieveAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


class CharacterListView(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class CharacterDetailView(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
