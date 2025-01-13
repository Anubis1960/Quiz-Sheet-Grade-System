import logging
from http import HTTPStatus
from src.util.encrypt import *
from src.models.teacher import Teacher
from src.services.teacher_service import create_teacher, get_teacher_by_email_and_password
from flask import redirect, url_for, session, Blueprint, request, jsonify, current_app

#
#   Authentification Blueprint
#
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def hello_world():
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as {email}!'


@auth_blueprint.route('/login', methods=['POST'])
def login() -> jsonify:
    # Handle login from the form
    if request.method == 'POST':
        # Fetch user credentials
        email = request.json.get('email')
        password = request.json.get('password')
        # Encrypt password for credentials verification
        encrypted_password = encrypt(password)

        # Credentials validation
        if email and password:
            session['email'] = email

            # Retrieve teacher based on email
            teacher_data = get_teacher_by_email_and_password(email, encrypted_password)

            if not teacher_data:
                return jsonify({'message': 'Invalid credentials'}), HTTPStatus.BAD_REQUEST

            return jsonify({
                            'message': 'Login Successfully',
                            'user_data': teacher_data
                            }), HTTPStatus.OK
        else:
            return jsonify({'message': 'Invalid credentials'}), HTTPStatus.BAD_REQUEST

    else:
        # Handle case when the user logs in via OAuth2.0
        google = current_app.oauth_manager.get_provider('google')
        redirect_uri = url_for('auth.authorize', _external=True)
        return google.authorize_redirect(redirect_uri)


@auth_blueprint.route('/authorize')
def authorize() -> jsonify:
    # Handle the OAuth callback from Google
    google = current_app.oauth_manager.get_provider('google')
    token = google.authorize_access_token()

    # Retrieve the access token
    access_token = token['access_token']
    resp = google.get('userinfo')

    # Retrieve user data
    user_info = resp.json()
    user_email = user_info['email']
    user_name = user_info['name']

    # Generate random password
    user_password = generate_random_password()
    # Encrypt the generated password
    user_password_encrypted = encrypt(user_password)

    # Insert the new user into db
    teacher_data = Teacher(user_name, user_email, user_password_encrypted)
    create_teacher(teacher_data)

    # Store email in session
    session['email'] = user_email

    # Make the session permanent
    session.permanent = True

    return jsonify({'message': 'Login Successfully via Google Auth',
                    'access_token': access_token, 
                    'user_data': teacher_data
                    }), HTTPStatus.OK


@auth_blueprint.route('/logout')
def logout() -> redirect:
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
