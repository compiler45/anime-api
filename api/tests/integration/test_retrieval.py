from rest_framework.test import APITestCase
from taggit.models import Tag

from api.models import Anime, Character


class APIRetrievalTestCaseBase(APITestCase):
    def setUp(self):
        Anime(
            name='Sword Art Online',
            year_began=2001,
            year_ended=2009,
            synopsis='Cool anime about MMOPRGs.'
        ).save()
        

class AnimeListAPITestCase(APIRetrievalTestCaseBase):

    def test_hitting_all_animes_endpoint_gives_200_status_code(self):
        response = self.client.get('/api/v1/animes/')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_number_of_results_equal_to_number_in_database(self):
        response_data = self.client.get('/api/v1/animes/').data
        self.assertEqual(len(response_data), Anime.objects.count())


class AnimeDetailAPITestCase(APIRetrievalTestCaseBase):

    def test_hitting_single_anime_endpoint_gives_200_status_code(self):
        response = self.client.get('/api/v1/animes/1/')

    def test_only_ever_get_one_result_for_detail_view(self):
        response_data = self.client.get('/api/v1/animes/').data
        self.assertEqual(len(response_data), 1)

    def test_response_contains_correct_details_of_requested_anime(self):
        anime_data = self.client.get('/api/v1/animes/1/').data
        anime = Anime.objects.get(id=1)
        self.assertEqual(anime_data['name'], anime.name)
        self.assertEqual(anime_data['year_began'], anime.year_began)
        self.assertEqual(anime_data['year_ended'], anime.year_ended)
        self.assertEqual(anime_data['synopsis'], anime.synopsis)

    def test_correct_fields_show_up_in_response(self):
        anime_data = self.client.get('/api/v1/animes/1/').data
        self.assertSetEqual(set(anime_data.keys()),
                             {
                                 'name',
                                 'year_ended',
                                 'year_began',
                                 'synopsis',
                                 'genres',
                                 'characters',
                             })

    def test_anime_genres_included_in_response(self):                       
        anime = Anime.objects.get(id=1)
        anime.genres.add(Tag.objects.create(name='seinen'))
        anime.save()
        
        anime_data = self.client.get('/api/v1/animes/1/').data
        genres = anime_data['genres']
        self.assertEqual(genres, ['seinen'])

    def test_anime_characters_should_have_name_and_id_in_response(self):
        anime = Anime.objects.get(id=1) 
        character = Character.objects.create(name='Kirito', description='SAO protagonist', gender='M', anime=anime)
        character.save()

        anime_data = self.client.get('/api/v1/animes/1/').data
        characters = anime_data['characters']
        self.assertEqual(
            characters,
            [{
                'id': 1,
                'name': 'Kirito',
            }]
        )
