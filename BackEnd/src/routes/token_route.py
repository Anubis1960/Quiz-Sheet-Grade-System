from http import HTTPStatus
from flask import Blueprint, request, jsonify

from src.services.teacher_service import get_teacher_by_id
from src.services.token_service import validate_teacher_token, generate_token, validate_url_token
from src.util.mail_gen import send_email

TOKEN_URL = '/api/token'

token_blueprint = Blueprint('token', __name__, url_prefix=TOKEN_URL)


@token_blueprint.route('/generate', methods=['POST'])
def generate() -> jsonify:
    """
    Generates a token for the teacher based on provided parameters.

    This endpoint accepts a POST request with the following JSON body:
    - `params`: Dictionary containing the parameters for the token.
    - `exp_time` (optional): The expiration time of the token in seconds (default is 3600 seconds, or 1 hour).

    The function generates a token and, if a teacher ID is provided, sends an email to the teacher with the token
    and expiration details.

    Returns:
        jsonify: The generated token in a JSON response.

    HTTPStatus:
        200 OK: On successful token generation.
        500 Internal Server Error: If an exception occurs.
    """
    try:
        data = request.get_json()
        params = data.get('params')
        exp_time = data.get('exp_time', 3600)

        token = generate_token(params, exp_time)

        teacher_id = params.get('id')
        if teacher_id:
            teacher = get_teacher_by_id(teacher_id)
            if teacher:
                send_email("Token Generated",
                           f"Your Token: \n {token} \n expires in {exp_time // 3600} hours", teacher['email'])

        return jsonify({
            'token': token
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@token_blueprint.route('/validate/<token>', methods=['GET'])
def validate_token_route(token: str) -> jsonify:
    """
    Validates the provided teacher token.

    This endpoint accepts a GET request where the token is passed in the URL path.

    Args:
        token (str): The token to be validated.

    Returns:
        jsonify: A JSON response indicating whether the token is valid or not.

    HTTPStatus:
        200 OK: If the token is valid.
        500 Internal Server Error: If an exception occurs during token validation.
    """
    try:
        validation = validate_teacher_token(token)
        return jsonify(validation), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@token_blueprint.route('/validate_url/<token>', methods=['GET'])
def validate_url_token_route(token: str) -> jsonify:
    """
    Validates the provided URL token.

    This endpoint accepts a GET request where the token is passed in the URL path.

    Args:
        token (str): The token to be validated.

    Returns:
        jsonify: A JSON response indicating whether the token is valid or not.

    HTTPStatus:
        200 OK: If the URL token is valid.
        500 Internal Server Error: If an exception occurs during URL token validation.
    """
    try:
        validation = validate_url_token(token)
        return jsonify(validation), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
