import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    """Tests pour les endpoints Review"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review_success(self):
        # Création de user et place pour associer
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
        })
        place_resp = self.client.post('/api/v1/places/', json={
            "name": "Lovely Place",
            "description": "Nice description"
        })
        user_id = user_resp.get_json()['id']
        place_id = place_resp.get_json()['id']

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,  # supposons que max=5
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
