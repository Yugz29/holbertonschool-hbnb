import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": 0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place(self):
        response = self.client.post('/api/v1/amenities/', json={
            "title": "Garage breton",
            "description": "Hotel pour garagistes",
            "price": 200.00,
            "latitude": 20.00,
            "longitude": 70.00,
            "owner_id": "string",
            "amenities": [
            "string"
            ]
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "title": "Les Gayeulles",
            "description": "Hotel de luxe plein-air",
            "price": 150.00,
            "latitude": 60.00,
            "longitude": 40.00,
            "owner_id": True,
            "amenities": [
            "string"
            ]
        })
        self.assertEqual(response.status_code, 400)