import pytest

from api.models import Anime, Character


@pytest.fixture
def create_twenty_animes(db):
    for i in range(20):
        Anime.objects.create(name=f'Anime {i}', year_began=1995, year_ended=2018,
                             synopsis=f'This is anime number {i}')


@pytest.fixture
def create_twenty_characters(db):
    anime = Anime.objects.create(name='Anime 1', year_began=1995, year_ended=2018)
    for i in range(20):
        Character.objects.create(name=f'Character {i}', description='A character', gender='F',
                                 anime=anime)
        

class PaginationTestCase:

    @pytest.mark.usefixtures("create_twenty_animes")
    def test_get_animes_with_more_than_ten_in_db_check_number_results_is_ten(self, client):
        response_data = client.get('/api/v1/animes/').data
        assert len(response_data['results']) == 10

    @pytest.mark.usefixtures("create_twenty_characters")
    def test_get_characters_with_more_than_ten_in_db_check_number_results_is_ten(self, client):
        response_data = client.get('/api/v1/characters/').data
        assert len(response_data['results']) == 10

    @pytest.mark.usefixtures("create_twenty_animes")
    def test_get_animes_with_page_param_equals_three_and_twenty_one_animes_check_number_results_is_one(
        self, client
    ):
        Anime.objects.create(name='Anime 21', year_began=1995, year_ended=2018)
        response_data = client.get('/api/v1/animes/?page=3').data
        assert len(response_data['results']) == 1

    @pytest.mark.usefixtures("create_twenty_characters")
    def test_get_characters_with_page_param_equals_three_and_twenty_one_characters_check_number_results_is_one(
        self, client
    ):
        Character.objects.create(name='Character 21', description='A character', gender='F',
                                 anime=Anime.objects.get(id=1))
        response_data = client.get('/api/v1/characters/?page=3').data
        assert len(response_data['results']) == 1
        
