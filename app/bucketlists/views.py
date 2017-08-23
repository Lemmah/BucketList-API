# app/bucketlists/views.py

from . import bucketlists_blueprint

import uuid
from app.models.bucketlists import Bucketlist, User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

# app.route: /bucketlists
class BucketlistsView(MethodView):
    ''' Handling the bucketlists endpoints '''

    def get(self):
        '''
        GET request for url: /bucketlist
        Get all bucketlists
        '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlists = Bucketlist.query.filter_by(created_by=user_id)
                results = []

                for bucketlist in bucketlists:
                    obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    results.append(obj)

                return make_response(jsonify(results)), 200

    def post(self):
        '''
        POST request for url: /bucketlist
        Create a bucketlist
        '''
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                name = str(request.data.get('name', ''))
                public_id = str(uuid.uuid4())
                if name:
                    bucketlist = Bucketlist(name=name,
                        created_by=user_id, public_id=public_id)
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'create_by': user_id
                        })
                    return make_response(response), 201


# app.route: /bucketlists/<int:id>
# --> Manipulating a specific already existing buckelist
class BucketlistView(MethodView):
    '''
    Facilitating manipulation of a bucketlist
    '''

    def get(self, id):
        ''' READ a bucketlist '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    abort(404)
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_createad': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'created_by': bucketlist.created_by
                    })
                return make_response(response), 200

        return ''

    def put(self, id):
        ''' UPDATE a bucketlist '''
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    abort(404)
                name = str(request.data.get('name', ''))

                bucketlist.name = name
                bucketlist.save()

                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'created_by': bucketlist.created_by
                }
                return make_response(jsonify(response)), 200

        response = jsonify({"message": "Token is missing"})
        return response

    def delete(self, id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    abort(404)
                bucketlist.delete()
                response = jsonify({"message": "bucketlist {} deleted".format(bucketlist.id)})
                return make_response(response), 200
        return ''


# Define the API resource
bucketlists_view = BucketlistsView.as_view('bucketlists_view')
bucketlist_view = BucketlistView.as_view('bucketlist_view')

# Define the rule for bucketlists operations
# Then add the rule to the blueprint
bucketlists_blueprint.add_url_rule(
    '/bucketlists',
    view_func=bucketlists_view,
    methods=['POST', 'GET'])
bucketlists_blueprint.add_url_rule(
    '/bucketlists/<int:id>',
    view_func=bucketlist_view,
    methods=['GET', 'PUT', 'DELETE'])


