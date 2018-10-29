from django.contrib.auth.models import User
from django.test import TestCase


class AdminViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='maetel',
                                                 email='maetel@galaxy.com',
                                                 password='fantasy')

    def test_can_reach_anime_section_on_admin_site(self):
        self.client.login(username='maetel', password='fantasy')
        response = self.client.get('/admin/api/anime/')
        self.assertEqual(response.status_code, 200)
    
    def test_can_reach_character_section_on_admin_site(self):
        resp = self.client.login(username='maetel', password='fantasy')
        response = self.client.get('/admin/api/character/')
        self.assertEqual(response.status_code, 200)
