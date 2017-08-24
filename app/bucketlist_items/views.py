# app/bucketlist_items/views.py

from . import bucketlist_items_blueprint

import uuid
from app.models.bucketlists import Bucketlist, BucketlistItem, User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

# app.route: /bucketlists
class BucketlistsView(MethodView):
    ''' Handling the bucketlists endpoints '''

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
                    obj = {
                        'id': bucketlist_item.id,
                        'name': bucketlist_item.name,
                        'date_created': bucketlist_item.date_created,
                        'date_modified': bucketlist_item.date_modified,
                        'belongs_to': bucketlist_item.belongs_to
                    }
                    results.append(obj)

                return make_response(jsonify(results)), 200

    def post(self, id):
        '''
        POST request for url: /bucketlist/<id>/items
        Create a bucketlist item
        '''
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                name = str(request.data.get('name', ''))
                if name:
                    # Ensuring no duplicate Bucketlist items.
                    bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, name=name).first()
                    if not bucketlist_item:
                        public_id = str(uuid.uuid4())
                        bucketlist_item = BucketlistItem(name=name,
                            belongs_to=id, public_id=public_id)
                        bucketlist_item.save()
                        response = jsonify({
                            'id': bucketlist_item.id,
                            'name': bucketlist_item.name,
                            'date_created': bucketlist_item.date_created,
                            'date_modified': bucketlist_item.date_modified,
                            'belongs_to': bucketlist_item.belongs_to
                            })
                        return make_response(response), 201
                    return make_response(jsonify({"message": "Bucketlist Item already exists"})), 409


# app.route: /bucketlists/<int:id>
# --> Manipulating a specific already existing buckelist
class BucketlistView(MethodView):
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
                    abort(404)
                response = jsonify({
                    'id': bucketlist_item.id,
                    'name': bucketlist_item.name,
                    'date_created': bucketlist_item.date_created,
                    'date_modified': bucketlist_item.date_modified,
                    'belongs_to': bucketlist_item.belongs_to
                    })
                return make_response(response), 200


    def put(self, id, item_id):
        ''' UPDATE a bucketlist '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, id=item_id).first()
                if not bucketlist_item:
                    return make_response(
                        jsonify({
                            "message": "The Item does not exist"
                            })), 404
                name = str(request.data.get('name', ''))

                bucketlist_item.name = name
                bucketlist_item.save()

                response = {
                    'id': bucketlist_item.id,
                    'name': bucketlist_item.name,
                    'date_created': bucketlist_item.date_created,
                    'date_modified': bucketlist_item.date_modified,
                    'belongs_to': bucketlist_item.belongs_to
                }
                return make_response(jsonify(response)), 200


    def delete(self, id, item_id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist_item = BucketlistItem.query.filter_by(belongs_to=id, id=item_id).first()
                if not bucketlist_item:
                    abort(404)
                bucketlist_item.delete()
                response = jsonify({"message": "bucketlist {} deleted".format(bucketlist_item.id)})
                return make_response(response), 200



# Define the API resource
bucketlist_items_view = BucketlistsView.as_view('bucketlists_view')
bucketlist_item_view = BucketlistView.as_view('bucketlist_view')

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


