Module src.routes.auth_route
============================

Functions
---------

`authorize() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Handle the OAuth callback from Google after the user grants permissions.
    
    Retrieves the user's information (email and name) from the OAuth provider, checks if the user exists in the database,
    and either creates a new user or logs the existing user in. Then, a token is generated for the user.
    
    Returns:
        redirect: Redirects to a callback URL with user data and token in the query parameters.

`hello_world()`
:   A test route to check if the user is logged in.
    
    This route simply returns a message with the logged-in user's email, if available.
    
    Returns:
        str: A greeting message with the logged-in user's email, or a default message.

`login() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Handle login requests. Supports both regular login and OAuth2.0 login via Google.
    
    On POST request, validates user credentials (email and password), creates a session, and returns a token.
    
    On GET request, redirects the user to the OAuth provider (Google).
    
    Returns:
        jsonify: A response containing user data and token on successful login or error message on failure.
        HTTPStatus: 200 OK if credentials are valid, 400 BAD REQUEST if invalid credentials are provided.

`logout() ‑> <function redirect at 0x000002A05DF179C0>`
:   Logs the user out by clearing the session.
    
    This route removes all keys from the session and then redirects the user to the home page.
    
    Returns:
        redirect: Redirects the user to the home page after logging out.