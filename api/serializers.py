from rest_framework import serializers

from api.models import Anime, Character


class CharacterSerializer(serializers.ModelSerializer):
    anime = serializers.StringRelatedField()
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Character
        fields = ('name', 'anime', 'description', 'gender')


class AnimeSerializer(serializers.ModelSerializer):
    # tags cannot be easily serialized by default
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
    
    def to_representation(self, anime_obj):
        resp = super().to_representation(anime_obj)
        # return the name and id for each character, not just the id
        character_ids = resp['characters']  
        new_character_resp = list()
        for character_id in character_ids:
            character = Character.objects.get(id=character_id)
            new_character_resp.append(
                {'id': character_id,
                 'name': character.name}
            )

        resp['characters'] = new_character_resp
        return resp
