from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import AnimeViewSet, CharacterViewSet

router = SimpleRouter()
router.register(r'v1/animes', AnimeViewSet)
router.register(r'v1/characters', CharacterViewSet)

urlpatterns = router.urls
