import unittest
import uuid
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    """Tests pour les endpoints Place"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Créer un owner pour le place
        owner_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": f"owner-{uuid.uuid4()}@example.com"
        })
        owner_data = owner_resp.get_json()
        self.assertIn('id', owner_data)
        self.owner_id = owner_data['id']

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -73.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_place_invalid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -10,
            "latitude": 100,
            "longitude": 200,
            "owner_id": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_place_success(self):
        post_resp = self.client.post('/api/v1/places/', json={
            "title": "Get Place",
            "description": "Retrieve place",
            "price": 50.0,
            "latitude": 40.0,
            "longitude": -70.0,
            "owner_id": self.owner_id
        })
        place_id = post_resp.get_json()['id']

        get_resp = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_resp.status_code, 200)

    def test_get_place_not_found(self):
        get_resp = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(get_resp.status_code, 404)

    def test_update_place_success(self):
        post_resp = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "description": "Old description",
            "price": 20.0,
            "latitude": 42.0,
            "longitude": -72.0,
            "owner_id": self.owner_id
        })
        place_id = post_resp.get_json()['id']

        put_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "description": "New description",
            "price": 30.0
        })
        self.assertEqual(put_resp.status_code, 200)

    def test_update_place_invalid(self):
        post_resp = self.client.post('/api/v1/places/', json={
            "title": "Sample Place",
            "description": "Sample",
            "price": 10.0,
            "latitude": 41.0,
            "longitude": -71.0,
            "owner_id": self.owner_id
        })
        place_id = post_resp.get_json()['id']

        put_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "",
            "price": -5
        })
        self.assertEqual(put_resp.status_code, 400)
        data = put_resp.get_json()
        self.assertIn('error', data)

    def test_update_place_not_found(self):
        put_resp = self.client.put('/api/v1/places/nonexistent-id', json={
            "title": "Update",
            "price": 50
        })
        self.assertEqual(put_resp.status_code, 404)

    def test_delete_place_success(self):
        post_resp = self.client.post('/api/v1/places/', json={
            "title": "Delete Place",
            "description": "To delete",
            "price": 15.0,
            "latitude": 43.0,
            "longitude": -74.0,
            "owner_id": self.owner_id
        })
        place_id = post_resp.get_json()['id']

        del_resp = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(del_resp.status_code, 200)

        get_resp = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_delete_place_not_found(self):
        del_resp = self.client.delete('/api/v1/places/nonexistent-id')
        self.assertEqual(del_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
