# app/bucketlists/views.py

from . import bucketlists_blueprint
from app.responses.responses import Response, Success, Error
import uuid
from app.models.bucketlists import Bucketlist, User
from flask import request, jsonify, abort, make_response
from flask.views import MethodView

# app.route: /bucketlists
class BucketlistsView(MethodView):
    ''' Handling the bucketlists endpoints '''

    def __init__(self):
        """ Instantiate my Custom Responses """
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    from app.decorators import token_required

    @token_required
    def get(self, user_id):
        '''
        GET request for url: /bucketlist
        Get all bucketlists
        '''
        bucketlists = Bucketlist.query.filter_by(created_by=user_id)
        results = []

        for bucketlist in bucketlists:
            obj = self.response.define_bucketlist(bucketlist)
            results.append(obj)

        return self.success.complete_request(results)
    
    @token_required        
    def post(self, user_id):
        '''
        POST request for url: /bucketlist
        Create a bucketlist
        '''
        # Get the access token from the header
        name = str(request.data.get('name', ''))
        public_id = str(uuid.uuid4())
        if name:
            bucketlist = Bucketlist.query.filter_by(name=name,
                created_by=user_id).first()
            if bucketlist:
                return self.error.causes_conflict("A Bucketlist with the same name already exists")
            bucketlist = Bucketlist(name=name,
                created_by=user_id, public_id=public_id)
            bucketlist.save()
            response = self.response.define_bucketlist(bucketlist)
            return self.success.create_resource(response)
        return self.error.not_acceptable("A bucketlist must have a name")


# app.route: /bucketlists/<int:id>
# --> Manipulating a specific already existing buckelist
class BucketlistView(BucketlistsView):
    '''
    Facilitating manipulation of a bucketlist
    '''

    from app.decorators import token_required

    @token_required
    def get(self, id, user_id):
        ''' READ a bucketlist '''
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
        if not bucketlist:
            return self.error.not_found("Bucketlist not found")
        response = self.response.define_bucketlist(bucketlist)
        return self.success.complete_request(response)

    @token_required
    def put(self, id, user_id):
        ''' UPDATE a bucketlist '''
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
        if not bucketlist:
            return self.error.not_found("Bucketlist not found")
        name = str(request.data.get('name', ''))
        bucketlist.name = name
        bucketlist.save()
        response = self.response.define_bucketlist(bucketlist)
        return self.success.complete_request(response)

    @token_required
    def delete(self, id, user_id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            return self.error.not_found("Bucketlist does not exist.")
        bucketlist.delete()
        response = "Bucketlist {} has been deleted.".format(bucketlist.id)
        return self.success.complete_request(response)


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


