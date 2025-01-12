from authlib.integrations.flask_client import OAuth
from flask import current_app

#######################
#
#	OAuth 2.0 Config - GOOGLE 
#
#######################
class OAuthManager:
	def __init__(self, app=None):
		self.oauth = OAuth()
		if app:
			self.init_app(app)
	
	def init_app(self, app):
		"""Initialize OAuth with the app configuration."""
		self.oauth.init_app(app)
		self.oauth.register(
			name='google',
			client_id='860148270648-qpgt1p8lr8fbali6svnsgifooj7eddac.apps.googleusercontent.com',
			client_secret='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',
			access_token_url='https://accounts.google.com/o/oauth2/token',
			access_token_params=None,
			authorize_url='https://accounts.google.com/o/oauth2/auth',
			authorize_params=None,
			api_base_url='https://www.googleapis.com/oauth2/v1/',
			# Usefull to fetch user info
			userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
			client_kwargs={'scope': 'email profile'},
			server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
		)

	def get_provider(self, name):
		"""Retrieve a registered OAuth provider by name."""
		return self.oauth.create_client(name)