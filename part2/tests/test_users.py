import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Tests pour les endpoints User"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_create_user_invalid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_user_success(self):
        post_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        })
        user_id = post_resp.get_json()['id']

        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'John')

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)


    def test_update_user_success(self):
        # Create user
        post_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
        })
        user_id = post_resp.get_json()['id']
        # Update user
        put_resp = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Alicia",
            "last_name": "Wonderland",
            "email": "alicia.wonderland@example.com"
        })
        self.assertEqual(put_resp.status_code, 200)
        data = put_resp.get_json()
        self.assertEqual(data['first_name'], 'Alicia')
        self.assertEqual(data['last_name'], 'Wonderland')

    def test_update_user_invalid_data(self):
        # Create user
        post_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com"
        })
        user_id = post_resp.get_json()['id']
        # Update user with invalid data
        put_resp = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "not-an-email"
        })
        self.assertEqual(put_resp.status_code, 400)
        data = put_resp.get_json()
        self.assertIn('error', data)

    def test_update_user_not_found(self):
        put_resp = self.client.put('/api/v1/users/nonexistent-id', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost.user@example.com"
        })
        self.assertEqual(put_resp.status_code, 404)

    def test_delete_user_success(self):
        # Create user
        post_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Charlie",
            "last_name": "Chaplin",
            "email": "charlie@example.com"
        })
        user_id = post_resp.get_json()['id']
        print("User ID to delete:", user_id, type(user_id))
        # Check user exists before deletion
        get_resp_before = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_resp_before.status_code, 200)
        # Delete user
        del_resp = self.client.delete(f'/api/v1/users/{user_id}')
        self.assertEqual(del_resp.status_code, 200)
        # Try to get deleted user
        get_resp = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_delete_user_not_found(self):
        del_resp = self.client.delete('/api/v1/users/nonexistent-id')
        self.assertEqual(del_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
