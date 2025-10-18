import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    """Tests pour les endpoints Place"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "name": "Test Place",
            "description": "A nice place"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Place')

    def test_create_place_invalid(self):
        response = self.client.post('/api/v1/places/', json={
            "name": "",
            "description": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
