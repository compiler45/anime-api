from django.test import TestCase
from taggit.models import Tag

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


    def test_anime_string_representation_is_equal_to_name(self):
       self.assertEqual(str(self.anime), 'Cowboy Bebop')

    def test_can_add_genres_to_an_anime(self):
        self.anime.genres.add("action", "adventure", "existential")
        self.assertEqual(len(self.anime.genres.all()), 3)

    def test_can_add_a_character_to_an_anime(self):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        spike.anime = self.anime
        spike.save()
        self.assertEqual(len(self.anime.characters.all()), 1)
    

class CharacterModelTestCase(TestCase):

    def test_character_string_representation_is_equal_to_name(self):
        spike = Character(
            name='Spike Spiegel',
            description='Cool bounty hunter on a lone search for a lost love...',
            gender='M'
        )
        self.assertEqual(str(spike), 'Spike Spiegel')

