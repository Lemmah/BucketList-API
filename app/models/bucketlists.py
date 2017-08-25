# app/models/users

from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


# app/models/bucketlists

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    public_id = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    bucketlist_items = db.relationship(
        'BucketlistItem', order_by='BucketlistItem.id', cascade="all, delete-orphan")

    def __init__(self, name, public_id, created_by):
        """initialize with name, public_id and user_id"""
        self.name = name
        self.public_id = public_id
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return Bucketlist.query.filter_by(created_by=user_id)
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

# app/models/bucketlists

class BucketlistItem(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlist_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    public_id = db.Column(db.String(255))
    belongs_to = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self, name, public_id, belongs_to):
        """initialize with name, public_id and user_id"""
        self.name = name
        self.public_id = public_id
        self.belongs_to = belongs_to

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(belongs_to):
        return BucketlistItem.query.filter_by(belongs_to=belongs_to)
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<BucketlistItem: {}>".format(self.name)
