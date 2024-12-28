from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask import send_file
from src.util.pdf_gen import generate_pdf
from src.models.question import Question
from src.services.quiz_service import *

#
#	Define URL for quizzes
#
QUIZ_URL = '/api/quizzes'
#
#   Quiz Blueprint
#
quiz_blueprint = Blueprint('quiz', __name__, url_prefix=QUIZ_URL)


#
#	Route to display list of quizzes
#
@quiz_blueprint.route('/', methods=['GET'])
def get_quizzes() -> jsonify:
    quizzes_data = get_quizzes_data()
    return jsonify(quizzes_data), HTTPStatus.OK


@quiz_blueprint.route("/<quiz_id>", methods=['GET'])
def get_quiz(quiz_id: str) -> jsonify:
    try:
        quiz = get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({"status": "error", "message":
                f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a quiz into the Firestore Database
#
@quiz_blueprint.route('/', methods=['POST'])
def add_quiz() -> jsonify:
    try:
        data = request.get_json()

        title = data.get('title')
        description = data.get('description')
        teacher = data.get('teacher')
        questions = data.get('questions', [])

        quiz = create_quiz(Quiz(title, description, teacher, [Question(**q) for q in questions]))

        if "error" in quiz:
            return jsonify({"status": "error", "message": quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(quiz), HTTPStatus.CREATED

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Update quiz route
#
@quiz_blueprint.route("/<quiz_id>", methods=['PUT'])
def update_quiz(quiz_id: str) -> jsonify:
    try:
        updated_data = request.get_json()
        updated_quiz = update_quiz_data(updated_data, quiz_id)

        if "error" in updated_quiz:
            return jsonify({"status": "error", "message": updated_quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(updated_quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Delete quiz route
#
@quiz_blueprint.route("/<quiz_id>", methods=['DELETE'])
def delete_quiz(quiz_id: str) -> jsonify:
    try:
        quiz = delete_quiz_by_id(quiz_id)

        if "error" in quiz:
            return jsonify({"status": "error", "message": quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/<quiz_id>/pdf", methods=['GET'])
def export_pdf(quiz_id: str) -> jsonify:
    try:
        quiz = get_quiz_by_id(quiz_id)

        if not quiz:
            return jsonify({"status": "error", "message":
                f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

        pdf_buffer = generate_pdf(quiz_id, quiz)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{quiz_id}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR