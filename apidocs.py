import os
from flasgger import Swagger
from app import create_app
from app.decorators import token_required

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
swagger = Swagger(app)

@app.route('/auth/register', methods=["POST"])
def register_user():
    """ endpoint returns registration details.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    """
@app.route('/auth/login', methods=["POST"])
def login_user():
    """ endpoint returns authorization details.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    """

@app.route("/bucketlists", methods=["GET"])
@token_required
def get_all_bucketlists():
    """endpoint returns a list of all user's bucketlists.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    """
@app.route("/bucketlists", methods=["POST"])
@token_required
def create_bucketlist():
    """endpoint creates bucketlist and returns it's details.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
    """
@app.route('/bucketlists/<int:bid>', methods=['PUT'])
@token_required
def update_bucketlist():
    """endpoint  updates bucketlist with new details.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

@app.route('/bucketlists/<int:bid>', methods=['GET'])
@token_required
def get_bucketlist_by_id():
    """endpoint gets bucketlist details by id.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route('/bucketlists/<int:bid>', methods=['DELETE'])
@token_required
def delete_a_bucketlist():
    """endpoint deletes a bucketlist by id.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

@app.route("/bucketlists/<int:id>/items", methods=["GET"])
@token_required
def get_all_bucketlist_items():
    """endpoint returns all items belonging to a specific bucketlist.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: string
        required: true
    """
@app.route("/bucketlists/<int:id>/items", methods=["POST"])
@token_required
def create_bucketlist_item():
    """endpoint creates a bucketlist item.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: string
        required: true
    """
@app.route("/bucketlists/<int:bid>/items/<int:item_id>", methods=["PUT"])
@token_required
def update_bucketlist_item():
    """endpoint updates a bucketlist item by id.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route("/bucketlists/<int:bid>/items/<int:item_id>", methods=["DELETE"])
@token_required
def delete_a_bucketlist_item():
    """endpoint deletes a bucketlist item by id.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route("/bucketlists/<int:bid>/items/<int:item_id>", methods=["GET"])
@token_required
def get_bucketlist_item_by_id():
    """endpoint returns a specific bucketlist item by id.
    Authorization is in format: 'Bearer access_token'
    Copy the access token from the message/response you get after login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)
