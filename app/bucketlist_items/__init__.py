# bucketlist_items/__init__.py

from flask import Blueprint

# This instance of a Blueprint that represents the bucketlist_items blueprint
bucketlist_items_blueprint = Blueprint('bucketlist_items', __name__)

from . import views