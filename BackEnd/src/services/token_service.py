import jwt
import time
from src.services.teacher_service import get_teacher_by_id
from src.util.mail_gen import send_email

EKEY = 'f98d5d2f2f0142e2a8b2d9db07d5a92f302b'


def generate_token(p: dict, exp_time=3600) -> str:
    payload = {
        'iat': time.time(),
        'exp': time.time() + exp_time,
        'params': p
    }

    token = jwt.encode(payload, EKEY, algorithm='HS256')

    teacher_id = p.get('id')
    if teacher_id:
        teacher = get_teacher_by_id(teacher_id)
        if teacher:
            send_email("Token Generated",
                       f"Your Token: \n {token} \n expires in {exp_time // 3600} hours", teacher['email'])

    return token


def validate_teacher_token(tk: str) -> dict:
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
    try:
        payload = jwt.decode(tk, EKEY, algorithms='HS256')
        if time.time() > payload['exp']:
            return {"error": "Token has expired."}
        return {"token": tk, "message": "Token is valid."}

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}
