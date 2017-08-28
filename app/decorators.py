from functools import wraps
from flask import request
from app.models.bucketlists import Bucketlist, User
from app.responses.responses import Response, Success, Error


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]
        if not access_token:
            return self.error.unauthorized(
        "Login to get authorized. If you had logged in, your session expired.")
        user_id = User.decode_token(access_token)
        if isinstance(user_id, str):
            return self.error.forbid_action("Token has been rejected")
        return f(*args, user_id=user_id, **kwargs)
    return decorated