from rest_framework import serializers

from api.models import Anime, Character


class CharacterSerializer(serializers.ModelSerializer):
    anime = serializers.StringRelatedField()
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Character
        fields = ('name', 'anime', 'description', 'gender')


class AnimeSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    characters = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = ('name', 'year_began', 'year_ended', 'synopsis',
                  'genres', 'characters')
        
    def get_genres(self, anime_obj):
        return [
            genre.name for genre in anime_obj.genres.all()
        ]
    
    def get_characters(self, anime_obj):
        return [
            {'id': character.id, 'name': character.name} for
            character in anime_obj.characters.all()
        ]
    
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        if resp['year_ended'] is None:
            resp['year_ended'] = 'N/A'

        return resp
