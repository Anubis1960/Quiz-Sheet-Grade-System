from http import HTTPStatus
from urllib.parse import urlencode

from flask import redirect, url_for, session, Blueprint, request, jsonify, current_app

from src.models.teacher import Teacher
from src.services.teacher_service import create_teacher, get_teacher_by_email_and_password, get_teacher_by_email
from src.services.token_service import generate_token
from src.util.encrypt import *

#
#   Authentication Blueprint
#
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def hello_world():
    """
    A test route to check if the user is logged in.

    This route simply returns a message with the logged-in user's email, if available.

    Returns:
        str: A greeting message with the logged-in user's email, or a default message.
    """
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as {email}!' if email else 'Hello, you are not logged in!'


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login() -> jsonify:
    """
    Handle login requests. Supports both regular login and OAuth2.0 login via Google.

    On POST request, validates user credentials (email and password), creates a session, and returns a token.

    On GET request, redirects the user to the OAuth provider (Google).

    Returns:
        jsonify: A response containing user data and token on successful login or error message on failure.
        HTTPStatus: 200 OK if credentials are valid, 400 BAD REQUEST if invalid credentials are provided.
    """
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

            # Generate token
            token = generate_token({'id': teacher_data['id']})

            return jsonify({
                'user_data': teacher_data,
                'token': token
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
    """
    Handle the OAuth callback from Google after the user grants permissions.

    Retrieves the user's information (email and name) from the OAuth provider, checks if the user exists in the database,
    and either creates a new user or logs the existing user in. Then, a token is generated for the user.

    Returns:
        redirect: Redirects to a callback URL with user data and token in the query parameters.
    """
    google = current_app.oauth_manager.get_provider('google')
    token = google.authorize_access_token()

    # Retrieve the access token
    access_token = token['access_token']
    resp = google.get('userinfo')

    # Retrieve user data
    user_info = resp.json()
    user_email = user_info['email']
    user_name = user_info['name']

    # Check if email already exists
    exist_teacher = get_teacher_by_email(user_email)

    if not exist_teacher:
        # Generate random password
        user_password = generate_random_password()

        # Encrypt the generated password
        user_password_encrypted = encrypt(user_password)

        # Insert the new user into db
        teacher_data = Teacher(user_name, user_email, user_password_encrypted)
        teacher = create_teacher(teacher_data)

        # Store email in session
        session['email'] = user_email

        # Make the session permanent
        session.permanent = True
    else:
        teacher = exist_teacher

    token = generate_token({'id': teacher['id']})

    # Serialize user data
    query_params = urlencode({
        "access_token": access_token,
        "user_data": teacher,
        "token": token,
    })

    callback_url = f"http://localhost:4200/auth/callback?{query_params}"
    return redirect(callback_url)


@auth_blueprint.route('/logout')
def logout() -> redirect:
    """
    Logs the user out by clearing the session.

    This route removes all keys from the session and then redirects the user to the home page.

    Returns:
        redirect: Redirects the user to the home page after logging out.
    """
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
