# bucketlists/__init__.py

from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
bucketlists_blueprint = Blueprint('bucketlists', __name__)

from . import views