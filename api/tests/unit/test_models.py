from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from api.models import Anime, Character


class AnimeModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.anime = Anime.objects.create(
            name='Cowboy Bebop',
            year_began=1997,
            year_ended=1998,
            synopsis='Awesome anime heavily featuring themes around existentialism, ennui and loneliness.'
        )

    def test_create_anime_check_string_representation_is_equal_to_name(self):
        self.assertEqual(str(self.anime), 'Cowboy Bebop')

    def test_update_anime_with_new_genres_check_database(self):
        self.anime.genres.add("action", "adventure", "existential")
        self.assertEqual(len(self.anime.genres.all()), 3)

    def test_add_character_with_valid_details_check_added_to_database(self):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        spike.anime = self.anime
        spike.save()
        self.assertEqual(len(self.anime.characters.all()), 1)

    def test_create_with_duplicate_name_check_integrity_error_is_thrown(self):
        self.assertRaises(
            IntegrityError,
            Anime.objects.create,
            name='Cowboy Bebop',
            year_began=1997,
            year_ended=1998,
            synopsis='Duplicate anime'
        )

    def test_create_with_year_ended_less_than_year_began_check_is_invalid(self):
        anime = Anime(name='Some Anime', year_began=1997, year_ended=1990, synopsis='A synopsis')
        try:
            anime.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict[NON_FIELD_ERRORS],
                             ['year_ended cannot be before year_began'])
        else:
            self.fail('ValidationError not raised for invalid Anime instance')

    def test_create_with_null_year_ended_check_is_valid(self):
        try:
            Anime.objects.create(name='Some Anime', year_began=1997, year_ended=None, synopsis='A synopsis')
        except Exception as e:
            self.fail('year_ended should be nullable. Received error {}'.format(e))


class CharacterModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.anime = Anime.objects.create(
            name='Cowboy Bebop',
            year_began=1997,
            year_ended=1998,
            synopsis='Awesome anime heavily featuring themes around existentialism, ennui and loneliness.'
        )

    def test_create_check_character_string_representation_is_equal_to_name(self):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        self.assertEqual(str(spike), 'Spike Spiegel')

    def test_create_with_same_character_in_same_anime_check_integrity_error_is_thrown(self):
        Character.objects.create(name='Jet', description='Arm-less bounty hunter',
                                 gender='M', anime=self.anime)
        self.assertRaises(
            IntegrityError,
            Character.objects.create,
            name='Jet',
            description='Another description',
            gender='M',
            anime=self.anime
        )
