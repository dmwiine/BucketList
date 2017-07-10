import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This is the bucketlist test case class"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Dance in a flash mob'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketlist_creation(self):
        """Test that the API can create a bucketlist (POST request)"""
        response = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Dance in a flash mob', str(response.data))

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get a bucketlist (GET request)."""
        response = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/bucketlists/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dance in a flash mob', str(response.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by using it's id."""
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Dance in a flash mob', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test that the API can edit an existing bucketlist. (PUT request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Go bungee jumping'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": 'Go bungee jumping whoop whoop'
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('whoop whoop', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Go bungee jumping'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()