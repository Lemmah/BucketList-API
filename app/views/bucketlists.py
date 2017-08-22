
""" REQUIRED ENDPOINTS
# User auth
@app.route('/api/auth/register', methods=['POST'])

@app.route('/api/auth/login', methods=['POST'])

@app.route('/api/auth/logout', methods=['POST'])

@app.route('/api/auth/reset-password', methods=['POST'])

# CRUD bucketlist
@app.route('/api/bucketlists/', methods=['POST'])

@app.route('/api/bucketlists/', methods=['GET'])

@app.route('/api/bucketlists/<id>', methods=['GET'])

@app.route('/api/bucketlists/<id>', methods=['PUT'])

@app.route('/api/bucketlists/<id>', methods=['DELETE'])

# CRUD bucketlist items
@app.route('/api/bucketlists/<id>/items/', methods=['POST'])

@app.route('/api/bucketlists/<id>/items/<item_id>', methods=['PUT'])

@app.route('/api/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
def delete_item(id,item_id):
    ''' Deleting a bucketlist item '''
    return 'This feature is yet to be implemented'
"""
import uuid
from app import app
from app.models.bucketlists import Bucketlist
from flask import request, jsonify, abort

# CRUD Bucketlists
@app.route('/bucketlists', methods=['POST'])
def create_bucketlist():
    name = str(request.data.get('name', ''))
    public_id = str(uuid.uuid4())
    if name:
        bucketlist = Bucketlist(name=name, public_id=public_id)
        bucketlist.save()
        response = jsonify({
            'id': bucketlist.public_id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 201
        return response

@app.route('/bucketlists', methods=['GET'])
def get_all_bucketlists():
    bucketlists = Bucketlist.get_all()
    results = []

    for bucketlist in bucketlists:
        obj = {
            'id': bucketlist.public_id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response

# Get a specific bucketlist, read it, update it or delete it   
@app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bucketlist_manipulation(id, **kwargs):
 # retrieve a buckelist using it's ID
    bucketlist = Bucketlist.query.filter_by(id=id).first()
    if not bucketlist:
        # Raise an HTTPException with a 404 not found status code
        abort(404)

    if request.method == 'DELETE':
        bucketlist.delete()
        return {
        "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
     }, 200

    elif request.method == 'PUT':
        name = str(request.data.get('name', ''))
        bucketlist.name = name
        bucketlist.save()
        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 200
        return response
    else:
        # GET one bucketlist
        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 200
        return response
