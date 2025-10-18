import unittest
from app import create_app
import uuid

class TestReviewEndpoints(unittest.TestCase):
    """Test suite for Review endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Créer un utilisateur reviewer avec email unique
        reviewer_email = f"reviewer_{uuid.uuid4().hex}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "email": reviewer_email,
            "first_name": "Reviewer",
            "last_name": "Test"
        })
        self.user = user_resp.get_json()
        self.assertIsNotNone(self.user, "User creation response JSON is None")
        self.assertIn("id", self.user, f"User creation failed: {self.user}")

        # Créer un owner avec email unique
        owner_email = f"owner_{uuid.uuid4().hex}@example.com"
        owner_resp = self.client.post('/api/v1/users/', json={
            "email": owner_email,
            "first_name": "Owner",
            "last_name": "Test"
        })
        self.owner = owner_resp.get_json()
        self.assertIsNotNone(self.owner, "Owner creation response JSON is None")
        self.assertIn("id", self.owner, f"Owner creation failed: {self.owner}")

        # Créer un place avec owner_id, title, description, price, latitude, longitude
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place to review",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner["id"]
        })
        self.place = place_resp.get_json()
        self.assertIsNotNone(self.place, "Place creation response JSON is None")
        self.assertIn("id", self.place, f"Place creation failed: {self.place}")

    def test_post_review_success(self):
        payload = {
            "text": "Amazing experience!",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        }
        resp = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], payload['text'])
        self.assertEqual(data['user_id'], self.user['id'])
        self.assertEqual(data['place_id'], self.place['id'])
        # self.assertIn('created_at', data)
        # self.assertIn('updated_at', data)

    def test_post_review_invalid(self):
        resp = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn('error', data)

    def test_get_review_success(self):
        review_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Nice location.",
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = review_resp.get_json()
        resp = self.client.get(f'/api/v1/reviews/{review["id"]}')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['id'], review['id'])
        self.assertEqual(data['text'], "Nice location.")
        self.assertEqual(data['user_id'], self.user['id'])
        self.assertEqual(data['place_id'], self.place['id'])
        # self.assertIn('created_at', data)
        # self.assertIn('updated_at', data)

    def test_get_review_not_found(self):
        resp = self.client.get('/api/v1/reviews/nonexistent')
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn('error', data)

    def test_delete_review_success(self):
        review_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Delete me.",
            "rating": 2,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = review_resp.get_json()
        resp = self.client.delete(f'/api/v1/reviews/{review["id"]}')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], "Review deleted successfully")
        get_resp = self.client.get(f'/api/v1/reviews/{review["id"]}')
        self.assertEqual(get_resp.status_code, 404)

    def test_delete_review_not_found(self):
        resp = self.client.delete('/api/v1/reviews/nonexistent')
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn('error', data)

    def test_put_review_success(self):
        """Test: Update a review successfully (endpoint returns message only)"""
        review_resp = self.client.post('/api/v1/reviews/', json={
            "text": "To update.",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = review_resp.get_json()
        resp = self.client.put(f'/api/v1/reviews/{review["id"]}', json={
            "text": "Updated review text.",
            "rating": 4
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Review updated successfully')

    def test_put_review_invalid(self):
        review_resp = self.client.post('/api/v1/reviews/', json={
            "text": "To fail update.",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        review = review_resp.get_json()
        resp = self.client.put(f'/api/v1/reviews/{review["id"]}', json={
            "rating": 99
        })
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn('error', data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
