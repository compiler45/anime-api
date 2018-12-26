from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

import pytest

from api.models import Anime, Character


@pytest.fixture
def anime(db):
    return Anime.objects.create(
        name='Cowboy Bebop',
        year_began=1997,
        year_ended=1998,
        synopsis='Awesome anime heavily featuring themes around existentialism, ennui and loneliness.'
    )


class AnimeModelTestCase:

    @pytest.mark.usefixtures("anime")
    def test_create_anime_check_string_representation_is_equal_to_name(self, anime):
        assert str(anime) == 'Cowboy Bebop'

    @pytest.mark.usefixtures("anime")
    def test_update_anime_with_new_genres_check_database(self, anime):
        anime.genres.add("action", "adventure", "existential")
        assert len(anime.genres.all()) == 3

    @pytest.mark.usefixtures("anime")
    def test_add_character_with_valid_details_check_added_to_database(self, anime):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        spike.anime = anime
        spike.save()
        assert len(anime.characters.all()) == 1

    def test_create_with_duplicate_name_check_integrity_error_is_thrown(self, anime):
        with pytest.raises(IntegrityError):
            Anime.objects.create(name='Cowboy Bebop',
                                 year_began=1997,
                                 year_ended=1998,
                                 synopsis='Duplicate anime')

    def test_create_with_year_ended_less_than_year_began_check_is_invalid(self, db):
        anime = Anime(name='Some Anime', year_began=1997, year_ended=1990, synopsis='A synopsis')
        with pytest.raises(ValidationError) as exc:
            anime.full_clean()
            assert exc.message_dict[NON_FIELD_ERRORS] == ['year_ended cannot be before year_began']

    def test_create_with_null_year_ended_check_is_valid(self, db):
        Anime.objects.create(
            name='Some Anime', year_began=1997, year_ended=None, synopsis='A synopsis')


class CharacterModelTestCase:

    def test_create_check_character_string_representation_is_equal_to_name(self):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        assert str(spike) == 'Spike Spiegel'

    @pytest.mark.usefixtures("anime")
    def test_create_with_same_character_in_same_anime_check_integrity_error_is_thrown(self, anime):
        Character.objects.create(name='Jet', description='Arm-less bounty hunter',
                                 gender='M', anime=anime)
        with pytest.raises(IntegrityError):
            # TODO: ensure message in exception is correct
            Character.objects.create(
                name='Jet',
                description='Another description',
                gender='M',
                anime=anime
            )
