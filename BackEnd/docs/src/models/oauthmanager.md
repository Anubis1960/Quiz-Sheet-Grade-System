Module src.models.oauthmanager
==============================

Classes
-------

`OAuthManager(app=None)`
:   Manages OAuth 2.0 authentication with external providers, in this case, Google.
    
    Attributes:
        oauth (OAuth): The OAuth object to handle the OAuth authentication flow.
    
    Initializes the OAuthManager object. Optionally initializes OAuth with the Flask app.
    
    Args:
        app (Flask, optional): A Flask app instance to initialize the OAuth object with. Defaults to None.

    ### Methods

    `get_provider(self, name)`
    :   Retrieves a registered OAuth provider by name.
        
        Args:
            name (str): The name of the OAuth provider.
        
        Returns:
            OAuthClient: The OAuth client associated with the provider.

    `init_app(self, app)`
    :   Initializes OAuth with the app configuration and registers the Google OAuth provider.
        
        Args:
            app (Flask): A Flask app instance to configure OAuth.