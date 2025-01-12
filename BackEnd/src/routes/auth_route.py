from flask import Flask, redirect, url_for, session, Blueprint, request, jsonify, current_app
from authlib.integrations.flask_client import OAuth

#
#   Authentification Blueprint
#
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def hello_world():
	email = dict(session).get('email', None)
	return f'Hello, you are logged in as {email}!'


@auth_blueprint.route('/login')
def login() -> redirect:
	# Create google client
	google = current_app.oauth_manager.get_provider('google')
	redirect_uri = url_for('auth.authorize', _external=True)
	return google.authorize_redirect(redirect_uri)


@auth_blueprint.route('/authorize')
def authorize() -> jsonify:
	# Create google client
	google = google = current_app.oauth_manager.get_provider('google')
	# Access token from google - DICT 
	token = google.authorize_access_token()
	# Retrieve the access token
	access_token = token['access_token']
	resp = google.get('userinfo')
	user_info = resp.json()
	email = user_info['email']
	session['email'] = user_info['email']

	# Keep the session permanant so it keeps existing after broweser gets closed
	session.permanent = True  
	return jsonify({'access_token': access_token, 'loggedin_mail': email})


@auth_blueprint.route('/logout')
def logout() -> redirect:
	for key in list(session.keys()):
		session.pop(key)
	return redirect('/')