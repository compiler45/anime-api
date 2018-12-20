from rest_framework.test import APITestCase
from taggit.models import Tag

from api.models import Anime, Character


class APIRetrievalTestCaseBase(APITestCase):

    @classmethod
    def setUpTestData(self):
        Anime.objects.create(
            name='Sword Art Online',
            year_began=2001,
            year_ended=2009,
            synopsis='Cool anime about MMOPRGs.'
        )


class AnimeListAPITestCase(APIRetrievalTestCaseBase):

    def test_get_check_endpoint_gives_200_status_code(self):
        response = self.client.get('/api/v1/animes/')
        assert response.status_code == 200

    def test_get_check_response_contains_number_of_results_equal_to_number_in_database(self):
        response_data = self.client.get('/api/v1/animes/').data
        assert len(response_data) == 1


class AnimeDetailAPITestCase(APIRetrievalTestCaseBase):

    def test_get_check_endpoint_gives_200_status_code(self):
        self.client.get('/api/v1/animes/1/')

    def test_get_check_only_one_result_in_response(self):
        response_data = self.client.get('/api/v1/animes/').data
        assert len(response_data) == 1

    def test_get_check_response_contains_correct_details_of_requested_anime(self):
        anime_data = self.client.get('/api/v1/animes/1/').data
        anime = Anime.objects.get(id=1)
        assert anime_data['name'] == anime.name
        assert anime_data['year_began'] == anime.year_began
        assert anime_data['year_ended'] == anime.year_ended
        assert anime_data['synopsis'] == anime.synopsis

    def test_get_check_correct_fields_show_up_in_response(self):
        anime_data = self.client.get('/api/v1/animes/1/').data
        assert set(anime_data.keys()) == {'name', 'year_ended', 'year_began', 'synopsis',
                                          'genres', 'characters'}

    def test_get_check_response_contains_right_genres(self):
        anime = Anime.objects.get(id=1)
        anime.genres.add(Tag.objects.create(name='seinen'))
        anime.save()
        
        anime_data = self.client.get('/api/v1/animes/1/').data
        genres = anime_data['genres']
        assert genres == ['seinen']

    def test_get_check_id_and_name_in_response(self):
        anime = Anime.objects.get(id=1)
        character = Character.objects.create(name='Kirito', description='SAO protagonist', gender='M', anime=anime)
        character.save()

        anime_data = self.client.get('/api/v1/animes/1/').data
        characters = anime_data['characters']
        assert characters == [{'id': 1, 'name': 'Kirito'}]

    def test_get_with_year_ended_set_to_null_check_value(self):
        """
        When an Anime has a None value for 'year_ended', the JSON
        value should be N/A
        """
        anime = Anime.objects.get(id=1)
        anime.year_ended = None
        anime.save()
        anime_data = self.client.get('/api/v1/animes/1/').data
        assert anime_data['year_ended'] == 'N/A'


class CharacterListAPITestCase(APIRetrievalTestCaseBase):

    def test_get_characters_check_response_length(self):
        anime = Anime.objects.get(id=1)
        Character.objects.create(name='Kirito', description='SAO protagonist', gender='M', anime=anime)
        Character.objects.create(name='Asuna', description='Another SAO protagonist', gender='F', anime=anime)
        resp = self.client.get('/api/v1/characters/').data
        assert len(resp) == 2


class CharacterAPIDetailTestCase(APIRetrievalTestCaseBase):

    def test_get_check_correct_details_returned(self):
        anime = Anime.objects.get(id=1)
        Character.objects.create(name='Kirito', description='SAO protagonist', gender='M', anime=anime)
        resp = self.client.get('/api/v1/characters/1/').data
        assert resp == {'name': 'Kirito',
                        'description': 'SAO protagonist',
                        'gender': 'Male',
                        'anime': anime.name}


