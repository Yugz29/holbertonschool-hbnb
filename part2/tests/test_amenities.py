"""
Tests unitaires pour les endpoints Amenity de l'API HBnB.
"""
import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    """Tests pour les endpoints Amenity"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Créer une amenity pour tests GET et DELETE
        resp = self.client.post('/api/v1/amenities/', json={"name": "Piscine"})
        data = resp.get_json() or {}
        self.amenity_id = data.get('id')
        if not self.amenity_id:
            raise Exception("Failed to create amenity in setUp: 'id' not found in response")

    def test_post_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json() or {}
        self.assertIn('id', data)
        self.assertEqual(data.get('name'), 'WiFi')

    def test_post_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)
        data = response.get_json() or {}
        self.assertIn('error', data)

    def test_get_amenity_success(self):
        response = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json() or {}
        self.assertIn('id', data)
        self.assertIn('name', data)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/notfoundid/')
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity_success(self):
        resp = self.client.post('/api/v1/amenities/', json={"name": "Sauna"})
        data = resp.get_json() or {}
        amenity_id = data.get('id')
        self.assertIsNotNone(amenity_id, "Failed to create amenity for delete test: 'id' not found")
        response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'elle n'existe plus
        response2 = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response2.status_code, 404)

    def test_delete_amenity_not_found(self):
        response = self.client.delete('/api/v1/amenities/notfoundid/')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_success(self):
        update_data = {"name": "Updated Amenity"}
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json() or {}
        self.assertIn('id', data)
        self.assertEqual(data.get('name'), "Updated Amenity")

    def test_update_amenity_invalid(self):
        update_data = {"name": ""}
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json() or {}
        self.assertIn('error', data)

if __name__ == "__main__":
    unittest.main(verbosity=2)
