from rest_framework import serializers

from api.models import Anime


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ('name', 'year_began', 'year_ended', 'synopsis')

