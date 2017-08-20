
from app import app

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