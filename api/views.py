from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.models import Anime, Character
from api.serializers import AnimeSerializer, CharacterSerializer

# Create your views here.


class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

class CharacterViewSet(ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

