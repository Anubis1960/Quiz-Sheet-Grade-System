import time
import jwt
from src.services.teacher_service import get_teacher_by_id

EKEY = 'f98d5d2f2f0142e2a8b2d9db07d5a92f302b'

"""
Service functions for generating and validating JWT tokens.
"""


def generate_token(p: dict, exp_time=3600) -> str:
    """
    Generate a JWT token with the provided payload and expiration time.

    Args:
        p (dict): The payload data to encode in the token.
        exp_time (int, optional): The expiration time in seconds. Defaults to 3600.

    Returns:
        str: The generated JWT token.
    """
    payload = {
        'iat': time.time(),
        'exp': time.time() + exp_time,
        'params': p
    }

    token = jwt.encode(payload, EKEY, algorithm='HS256')

    return token


def validate_teacher_token(tk: str) -> dict:
    """
    Validate a JWT token and check if it belongs to a valid teacher.

    Args:
        tk (str): The JWT token to validate.

    Returns:
        dict: A dictionary containing the validation result or an error message.
    """
    try:
        payload = jwt.decode(tk, EKEY, algorithms='HS256')

        if time.time() > payload['exp']:
            return {"error": "Token has expired."}

        params = payload['params']
        t_id = params.get('id')
        teacher = get_teacher_by_id(t_id)

        if teacher == {}:
            return {"error": "Teacher not found."}

        return {"token": tk, "message": "Token is valid."}

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}


def validate_url_token(tk: str) -> dict:
    """
    Validate a JWT token without additional checks.

    Args:
        tk (str): The JWT token to validate.

    Returns:
        dict: A dictionary containing the validation result or an error message.
    """
    try:
        payload = jwt.decode(tk, EKEY, algorithms='HS256')

        if time.time() > payload['exp']:
            return {"error": "Token has expired."}

        return {"token": tk, "message": "Token is valid."}

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}
