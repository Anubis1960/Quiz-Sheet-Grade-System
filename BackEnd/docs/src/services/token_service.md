Module src.services.token_service
=================================

Variables
---------

`EKEY`
:   Service functions for generating and validating JWT tokens.

Functions
---------

`generate_token(p: dict, exp_time=3600) ‑> str`
:   Generate a JWT token with the provided payload and expiration time.
    
    Args:
        p (dict): The payload data to encode in the token.
        exp_time (int, optional): The expiration time in seconds. Defaults to 3600.
    
    Returns:
        str: The generated JWT token.

`validate_teacher_token(tk: str) ‑> dict`
:   Validate a JWT token and check if it belongs to a valid teacher.
    
    Args:
        tk (str): The JWT token to validate.
    
    Returns:
        dict: A dictionary containing the validation result or an error message.

`validate_url_token(tk: str) ‑> dict`
:   Validate a JWT token without additional checks.
    
    Args:
        tk (str): The JWT token to validate.
    
    Returns:
        dict: A dictionary containing the validation result or an error message.