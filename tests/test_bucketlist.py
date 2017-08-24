# tests/test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacation'}
        self.bucketlist_item = {'name': 'See the Hills There'}
        self.bucketlist_item1 = {'name': 'Propose to Her'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def create_bucketlist(self):
        """ Important for testing creation of bucketlist items """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        return (res,access_token)

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.create_bucketlist()[0]
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        # Create a bucketlist first
        res, access_token = self.create_bucketlist()
        self.assertEqual(res.status_code, 201)

        # get all the bucketlists that belong to the test user by making a GET request
        res = self.client().get(
            '/bucketlists',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        rv, access_token = self.create_bucketlist()

        # assert that the bucketlist is created 
        self.assertEqual(rv.status_code, 201)
        # get the response data in json format
        results = json.loads(rv.data.decode())

        result = self.client().get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        # assert that the bucketlist is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv, access_token = self.create_bucketlist()
        self.assertEqual(rv.status_code, 201)
        # get the json with the bucketlist
        results = json.loads(rv.data.decode())

        # then, we edit the created bucketlist by making a PUT request
        rv = self.client().put(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edited bucketlist to see if it is actually edited.
        results = self.client().get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        rv, access_token = self.create_bucketlist()
        # get the bucketlist in json
        results = json.loads(rv.data.decode())

        # delete the bucketlist we just created
        res = self.client().delete(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

        # Edge case: Test double deletion
        res = self.client().delete(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 404)

    # Some Common Edge Cases
    def test_creation_of_duplicate_bucketlist(self):
        """ Ensure Duplicate Bucketlists Cannot be Created """
        create_bucketlist = self.create_bucketlist()[0]
        self.assertEqual(create_bucketlist.status_code, 201)
        create_duplicate = self.create_bucketlist()[0]
        # Assert that this action causes conflict
        self.assertEqual(create_duplicate.status_code, 409)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()