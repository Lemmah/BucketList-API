# Extend testing of bucketlist
from . import test_bucketlist
import json

class TestBucketlistItem(test_bucketlist.BucketlistTestCase):
    """
    Testing Bucketlist Items which are in a bucketlist
    """

    def create_bucketlist_item(self, item_details):
        """ Important for Creation of items multiple times """
        res, access_token = self.create_bucketlist()
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        # Request to add an item to it
        rv = self.client().post(
            '/bucketlists/{}/items'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist_item)
        return (res, access_token, rv)

    def test_bucketlist_item_creation(self):
        """ Test if API can add items to bucketlist """
        # First, Create a Bucketlist
        res, access_token, rv = self.create_bucketlist_item(self.bucketlist_item)
        self.assertEqual(rv.status_code, 201)


    def test_api_can_get_all_buckelist_items(self):
        """ Test if API can get all items in a Bucketlist """
        pass
    def test_api_can_get_one_item_using_id(self):
        """ Test if API can get a specific item in a Bucketlist """
        pass
    def test_bucketlist_item_can_be_edited(self):
        """ Test if API can edit details of an item """
        pass
    def test_api_can_delete_an_item(self):
        """ Test if API can delete items from a bucketlist """
        pass
