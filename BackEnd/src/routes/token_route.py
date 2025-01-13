from http import HTTPStatus
from flask import Blueprint, request, jsonify
from src.services.token_service import get_tokenized_url, validate_token

TOKEN_URL = '/api/token'

token_blueprint = Blueprint('token', __name__, url_prefix=TOKEN_URL)


@token_blueprint.route('/generate', methods=['POST'])
def generate_token() -> jsonify:
    try:
        data = request.get_json()
        params = data.get('params')
        exp_time = data.get('exp_time', 3600)

        token = get_tokenized_url(params, exp_time)

        return jsonify({
            'token': token
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@token_blueprint.route('/validate/<token>', methods=['GET'])
def validate_token_route(token: str) -> jsonify:
    try:
        validation = validate_token(token)
        return jsonify(validation), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
