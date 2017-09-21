# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from flask_cors import CORS
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # The Bucketlists Endpoints as a blue print
    from .bucketlists import bucketlists_blueprint
    app.register_blueprint(bucketlists_blueprint)

    # The Bucketlist Items Endpoints registration
    from .bucketlist_items import bucketlist_items_blueprint
    app.register_blueprint(bucketlist_items_blueprint)
    # The Authentication Blue Print
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

