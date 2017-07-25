import re
from api.v1.models import User
from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /api/v1/auth/register"""

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                email = post_data['email'].strip()
                password = post_data['password'].strip()
                if not EMAIL_REGEX.match(email):
                    response = jsonify({
                    'error': 'Please enter a valid email',
                    'status_code': '400'
                    })
                    response.status_code = 400
                    return response

                if len(password) < 6:
                    response = jsonify({
                        'Error': 'Invalid password, it must be more than 6 characters',
                        'status_code': '400'
                        })
                    response.status_code = 400
                    return response

                user = User(email=email, password=password)
                user.save()

                response = {
                    'status': 'success',
                    'message': 'You registered successfully. Please log in.'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'status': 'fail',
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /api/v1/auth/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()
            if user and user.is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again',
                    'status_code': '401'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']
)
