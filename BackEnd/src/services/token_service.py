import jwt
import time
from urllib.parse import urlencode
from src.services.teacher_service import get_teacher_by_id

EKEY = 'f98d5d2f2f0142e2a8b2d9db07d5a92f302b'


def generate_token(p: dict, exp_time=3600) -> str:
    payload = {
        'iat': time.time(),
        'exp': time.time() + exp_time,
        'params': p
    }

    token = jwt.encode(payload, EKEY, algorithm='HS256')

    return token


def validate_token(tk: str) -> dict:
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
