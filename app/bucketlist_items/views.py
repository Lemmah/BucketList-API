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

    def get(self,id):
        '''
        GET request for url: /bucketlist/<bucketlist_id>/items
        Get all bucketlist items
        '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist_items = BucketlistItem.get_all(belongs_to=id)
                results = []
                for bucketlist_item in bucketlist_items:
                    obj = self.response.define_bucketlist_item(bucketlist_item)
                    results.append(obj)
                return self.success.complete_request(results)
            return self.error.forbid_action("Token has been rejected")
        return self.unauthorized("Login to get access token")

    def post(self, id):
        '''
        POST request for url: /bucketlist/<id>/items
        Create a bucketlist item
        '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
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
            return self.error.forbid_action("Token has been rejected")
        return self.error.unauthorized("Login to get access token")


# app.route: /bucketlists/<int:id>
# --> Manipulating a specific already existing buckelist
class BucketlistItemView(BucketlistItemsView):
    '''
    Facilitating manipulation of a bucketlist
    '''

    def get(self, id, item_id):
        ''' READ a bucketlist item '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, id=item_id).first()
                if not bucketlist_item:
                    return self.error.not_found("Bucketlist not found")
                response = self.response.define_bucketlist_item(bucketlist_item)
                return self.success.complete_request(response)
            return self.error.forbid_action("Token has been rejected")
        return self.error.unauthorized("Login to get an access token")


    def put(self, id, item_id):
        ''' UPDATE a bucketlist '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
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
            return self.error.forbid_action("Token has been rejected")
        return self.error.unauthorized("Login to get an access token")


    def delete(self, id, item_id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id,
                    id=item_id).first()
                if not bucketlist_item:
                    return self.error.not_found("Bucketlist Item does not exist")
                bucketlist_item.delete()
                response = "Bucketlist Item {} has been deleted".format(item_id)
                return self.success.complete_request(response)
            return self.error.forbid_action("Token has been rejected")
        return self.error.unauthorized("Login to get an access token")



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


