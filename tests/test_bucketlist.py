import unittest
import os
import json
from api import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This is the bucketlist test case class"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Dance in a flash mob'}

        # binds the app to the current context
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        """Test that the API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        response = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully Created', str(response.data))

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        response = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 200)

        response = self.client().get(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Dance in a flash mob', str(response.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(rv.status_code, 200)
        result_in_json = json.loads(rv.data.decode())
        result = self.client().get(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Dance in a flash mob', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test that the API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go bungee jumping'})
        self.assertEqual(rv.status_code, 200)
        rv = self.client().put(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": 'Go bungee jumping whoop whoop'
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token)
            )
        self.assertIn('whoop whoop', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go bungee jumping'})
        self.assertEqual(rv.status_code, 200)
        res = self.client().delete(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token)
            )
        self.assertEqual(res.status_code, 200)
        results = self.client().get(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token)
            )
        print(results)
        self.assertEqual(results.status_code, 404)

    def test_api_can_add_item_to_bucketlist(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        response = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 200)
        item_response = self.client().post(
            '/api/v1/bucketlists/1/items/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go white water rafting'}
        )
        self.assertEqual(item_response.status_code, 200)
        self.assertIn('Bucketlist item successfully Created', str(item_response.data))

    def test_api_can_edit_item_in_bucketlist(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        response = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 200)
        item_response = self.client().post(
            '/api/v1/bucketlists/1/items/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go white water rafting'}
        )
        self.assertEqual(item_response.status_code, 200)
        self.assertIn('Bucketlist item successfully Created', str(item_response.data))
        item_response = self.client().put(
            '/api/v1/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go white water rafting on the nile'}
        )
        self.assertEqual(item_response.status_code, 200)
    
    def test_api_can_delete_item_from_bucketlist(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        response = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 200)
        item_response = self.client().post(
            '/api/v1/bucketlists/1/items/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go white water rafting'}
        )
        self.assertEqual(item_response.status_code, 200)
        self.assertIn('Bucketlist item successfully Created', str(item_response.data))
        item_response = self.client().delete(
            '/api/v1/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(item_response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
    