# Extend testing of bucketlist
from . import test_bucketlist
import json

class TestBucketlistItem(test_bucketlist.BucketlistTestCase):
    """
    Testing Bucketlist Items which are in a bucketlist
    """

    def create_bucketlist_item(self, *args):
        """ Important for Creation of items multiple times """
        res, access_token = self.create_bucketlist()
        results = json.loads(res.data.decode())
        try:
            bucketlist_id = results['id']
        # Occurence of KeyError means that:
        # the request just returned an error
        # I expect a conflict error if the item already exists
        except KeyError:
            bucketlist_id = args[1]

        finally:
            # Request to add an item to it
            rv = self.client().post(
                '/bucketlists/{}/items'.format(bucketlist_id),
                headers=dict(Authorization="Bearer " + access_token),
                data=args[0])
            return (access_token, rv, bucketlist_id)

    def test_bucketlist_item_creation(self):
        """ Test if API can add items to bucketlist """
        # First, Create a Bucketlist
        rv, bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)[1:3]
        self.assertEqual(rv.status_code, 201)
        self.assertIn('See the Hills There', str(rv.data))
        


    def test_api_can_get_all_buckelist_items(self):
        """ Test if API can get all items in a Bucketlist """
        # Create First Item
        access_token, rv, \
        bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)
        # Create Second Item
        access_token, rv, \
        bucketlist_id = self.create_bucketlist_item(self.bucketlist_item1,
            bucketlist_id)
        self.assertEqual(rv.status_code, 201)
        res = self.client().get(
            '/bucketlists/{}/items'.format(bucketlist_id),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test for first item
        self.assertIn('See the Hills', str(res.data))
        # Test for second item
        self.assertIn('Propose', str(res.data))

    def test_api_can_get_one_item_using_id(self):
        """ Test if API can get a specific item in a Bucketlist """
        # First Create an Item
        access_token, rv, \
        bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result = self.client().get(
            '/bucketlists/{}/items/{}'.format(bucketlist_id, results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)



    def test_bucketlist_item_can_be_edited(self):
        """ Test if API can edit details of an item """
        # First Create an Item
        access_token, rv, \
        bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result = self.client().put(
            '/bucketlists/{}/items/{}'.format(bucketlist_id, results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist_item1)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Propose', str(result.data))


    def test_api_can_delete_an_item(self):
        """ Test if API can delete items from a bucketlist """
        # First Create an Item
        access_token, rv, \
        bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result = self.client().delete(
            '/bucketlists/{}/items/{}'.format(bucketlist_id, results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist_item1)
        self.assertEqual(result.status_code, 200)
        # Try getting deleted bucketlist
        result = self.client().get(
            '/bucketlists/{}/items/{}'.format(bucketlist_id, results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_creation_of_duplicate_bucketlist_items(self):
        """ Ensure API forbids creation of duplicate items """
        rv, bucketlist_id = self.create_bucketlist_item(self.bucketlist_item)[1:3]
        self.assertEqual(rv.status_code, 201)
        self.assertIn('See the Hills There', str(rv.data))
        rv = self.create_bucketlist_item(self.bucketlist_item, bucketlist_id)[1]
        # Assert that duplication causes conflict
        self.assertEqual(rv.status_code, 409)
