# /app/auth/views.py

from . import auth_blueprint
from app.responses.responses import Response, Success, Error
from flask.views import MethodView
from flask import request
from app.models.bucketlists import User
import re

class RegistrationView(MethodView):
    """This class registers a new user."""
    def __init__(self):
        super().__init__()
        self.response = Response()
        self.error = Error()
        self.success = Success()

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        # Query to see if the user already exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                # Register the user
                email = post_data['email'].strip()
                password = post_data['password'].strip()

                # check registration without password
                if not password:
                    return self.error.not_acceptable(
                        "You can't register without a password")

                # check password length
                if len(password) < 8:
                    return self.error.not_acceptable(
                        "Password is too short. Minimum is 8 characters")

                # check email is not empty
                if not email:
                    return self.error.not_acceptable(
                        "You cannot register without an email")
                    
                # check correct format
                regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                if not re.match(regex, email):
                    return self.error.not_acceptable(
                        "The email address input is not valid")

                # Register user finally
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return self.success.create_resource(response)
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                return self.error.internal_server_error(str(e))
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            return self.error.not_acceptable("User already exists. Please login.")
            
class LoginView(RegistrationView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(email=request.data['email']).first()
            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'info': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return self.success.complete_request(response)
            else:
                return self.error.unauthorized("Invalid email or password, Please try again")

        except Exception as e:
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return self.error.internal_server_error(str(e))

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)