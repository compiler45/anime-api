from rest_framework import status
from taggit.models import Tag

import pytest

from api.models import Anime, Character
from api.tests.mixins import DetailViewTestCasePermissionsMixin, ListViewTestCasePermissionsMixin


@pytest.fixture(autouse=True)
def anime(db):
    return Anime.objects.create(name='Sword Art Online', year_began=2001,
                                year_ended=2009, synopsis='Cool anime about MMOPRGs.')


@pytest.fixture
def kirito(anime):
    Character.objects.create(name='Kirito', description='SAO protagonist', gender='M',
                             anime=anime)

    
class AnimeListAPITestCase(ListViewTestCasePermissionsMixin):
    URL = '/api/v1/animes/'
    
    def test_get_check_endpoint_gives_200_status_code(self, client):
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK

    def test_get_check_response_contains_number_of_results_equal_to_number_in_database(self, client):
        response_data = client.get(self.URL).data
        assert len(response_data['results']) == 1


class AnimeDetailAPITestCase(DetailViewTestCasePermissionsMixin):
    URL = '/api/v1/animes/1/'

    def test_get_check_endpoint_gives_200_status_code(self, client):
        client.get(self.URL)

    def test_get_check_only_one_result_in_response(self, client):
        response_data = client.get(self.URL).data
        assert isinstance(response_data, dict)

    @pytest.mark.django_db
    def test_get_check_response_contains_correct_details_of_requested_anime(self, client):
        anime_data = client.get(self.URL).data
        anime = Anime.objects.get(id=1)
        assert anime_data['name'] == anime.name
        assert anime_data['year_began'] == anime.year_began
        assert anime_data['year_ended'] == anime.year_ended
        assert anime_data['synopsis'] == anime.synopsis

    def test_get_check_correct_fields_show_up_in_response(self, client):
        anime_data = client.get(self.URL).data
        assert set(anime_data.keys()) == {'name', 'year_ended', 'year_began', 'synopsis',
                                          'genres', 'characters'}

    @pytest.mark.django_db
    def test_get_check_response_contains_right_genres(self, client):
        anime = Anime.objects.get(id=1)
        anime.genres.add(Tag.objects.create(name='seinen'))
        anime.save()
        
        anime_data = client.get(self.URL).data
        genres = anime_data['genres']
        assert genres == ['seinen']

    def test_get_check_id_and_name_in_response(self, client):
        anime = Anime.objects.get(id=1)
        character = Character.objects.create(name='Kirito', description='SAO protagonist', gender='M', anime=anime)
        character.save()

        anime_data = client.get(self.URL).data
        characters = anime_data['characters']
        assert characters == [{'id': 1, 'name': 'Kirito'}]

    @pytest.mark.django_db
    def test_get_with_year_ended_set_to_null_check_value(self, client):
        """
        When an Anime has a None value for 'year_ended', the JSON
        value should be N/A
        """
        anime = Anime.objects.get(id=1)
        anime.year_ended = None
        anime.save()
        anime_data = client.get(self.URL).data
        assert anime_data['year_ended'] == 'N/A'


class CharacterListAPITestCase(ListViewTestCasePermissionsMixin):
    URL = '/api/v1/characters/'

    def test_get_characters_check_response_length(self, client, kirito):
        anime = Anime.objects.get(id=1)
        Character.objects.create(name='Asuna', description='Another SAO protagonist', gender='F', anime=anime)
        resp = client.get(self.URL).data
        assert len(resp['results']) == 2


class CharacterAPIDetailTestCase(DetailViewTestCasePermissionsMixin):
    URL = '/api/v1/characters/1/'

    def test_get_check_correct_details_returned(self, client, kirito):
        anime = Anime.objects.get(id=1)
        resp = client.get(self.URL).data
        assert resp == {'name': 'Kirito',
                        'description': 'SAO protagonist',
                        'gender': 'Male',
                        'anime': anime.name}


