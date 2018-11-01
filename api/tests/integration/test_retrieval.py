from rest_framework.test import APITestCase


class AnimeRetrieveAPITestCase(APITestCase):

    def test_hitting_all_animes_endpoint_gives_200_status_code(self):
        response = self.client.get('/api/v1/animes/')
        self.assertEqual(response.status_code, 200)
