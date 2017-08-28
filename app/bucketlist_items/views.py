# app/bucketlist_items/views.py

from . import bucketlist_items_blueprint
from app.responses.responses import Response, Success, Error
import uuid
from app.models.bucketlists import Bucketlist, BucketlistItem, User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

# app.route: /bucketlists
class BucketlistItemsView(MethodView):
    ''' Handling the bucketlists endpoints '''
    
    def __init__(self):
        super().__init__()
        self.response = Response()
        self.error = Error()
        self.success = Success()

    from app.decorators import token_required

    @token_required
    def get(self, id, user_id):
        '''
        GET request for url: /bucketlist/<bucketlist_id>/items
        Get all bucketlist items
        '''
        bucketlist_items = BucketlistItem.get_all(belongs_to=id)
        results = []
        for bucketlist_item in bucketlist_items:
            obj = self.response.define_bucketlist_item(bucketlist_item)
            results.append(obj)
        return self.success.complete_request(results)
     
    @token_required   
    def post(self, id, user_id):
        '''
        POST request for url: /bucketlist/<id>/items
        Create a bucketlist item
        '''
        name = str(request.data.get('name', ''))
        if name:
            bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, name=name).first()
            if not bucketlist_item:
                public_id = str(uuid.uuid4())
                bucketlist_item = BucketlistItem(name=name,
                    belongs_to=id, public_id=public_id)
                bucketlist_item.save()
                response = self.response.define_bucketlist_item(bucketlist_item)
                return self.success.create_resource(response)
            return self.error.causes_conflict("Bucketlist Item already exists")
        return self.error.not_acceptable("Bucketlist Item must have a name")

# app.route: /bucketlists/<int:id>
# --> Manipulating a specific already existing buckelist
class BucketlistItemView(BucketlistItemsView):
    '''
    Facilitating manipulation of a bucketlist
    '''

    from app.decorators import token_required

    @token_required
    def get(self, id, item_id, user_id):
        ''' READ a bucketlist item '''
        bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, id=item_id).first()
        if not bucketlist_item:
            return self.error.not_found("Bucketlist not found")
        response = self.response.define_bucketlist_item(bucketlist_item)
        return self.success.complete_request(response)

    @token_required
    def put(self, id, item_id, user_id):
        ''' UPDATE a bucketlist '''
        bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id,
            id=item_id).first()
        if not bucketlist_item:
            return self.error.not_found("Bucketlist Item does not exist")
        name = str(request.data.get('name', ''))
        if name:
            bucketlist_item.name = name
            bucketlist_item.save()
            response = self.response.define_bucketlist_item(bucketlist_item)
        return self.success.complete_request(response)

    @token_required
    def delete(self, id, item_id, user_id):
        bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id,
            id=item_id).first()
        if not bucketlist_item:
            return self.error.not_found("Bucketlist Item does not exist")
        bucketlist_item.delete()
        response = "Bucketlist Item {} has been deleted".format(item_id)
        return self.success.complete_request(response)
           

# Define the API resource
bucketlist_items_view = BucketlistItemsView.as_view('bucketlists_view')
bucketlist_item_view = BucketlistItemView.as_view('bucketlist_view')

# Define the rule for bucketlists operations
# Then add the rule to the blueprint
bucketlist_items_blueprint.add_url_rule(
    '/bucketlists/<int:id>/items',
    view_func=bucketlist_items_view,
    methods=['POST', 'GET'])
bucketlist_items_blueprint.add_url_rule(
    '/bucketlists/<int:id>/items/<int:item_id>',
    view_func=bucketlist_item_view,
    methods=['GET', 'PUT', 'DELETE'])


