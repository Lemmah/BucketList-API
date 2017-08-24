# Extend testing of bucketlist
from . import test_bucketlist

class TestBucketlistItem(test_bucketlist.BucketlistTestCase):
    """
    Testing Bucketlist Items which are in a bucketlist
    """
    def test_bucketlist_item_creation(self):
        """ Test if API can add items to bucketlist """
        
        pass
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
