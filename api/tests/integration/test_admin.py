from django.contrib.auth.models import User
from django.test import TestCase

import pytest


@pytest.fixture(autouse=True)
def login(client, admin_user):
    client.login(username="admin", password="password")


class AdminViewTestCase:

    def test_can_reach_anime_section_on_admin_site(self, client, admin_user):
        response = client.get('/admin/api/anime/')
        assert response.status_code == 200
    
    def test_can_reach_character_section_on_admin_site(self, client, admin_user):
        response = client.get('/admin/api/character/')
        assert response.status_code == 200

