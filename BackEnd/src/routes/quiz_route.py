from http import HTTPStatus
from flask import Blueprint, request, jsonify

from src.exceptions import NoDataFoundError
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
    logging.info("\tRoutes Layer ==>	Requesting quizzes list loading...")
    try:
        # Retrieve quizzes
        quizzes_data = get_quizzes_data()

        # Verify if data exists
        if quizzes_data is []:
            return jsonify({"status:": "error",
                            "message": "No quizzes available"}), HTTPStatus.NOT_FOUND

        return jsonify(quizzes_data), HTTPStatus.OK

    except NoDataFoundError as e:
        return jsonify({"status": "error",
                        "message": str(e)}), HTTPStatus.NOT_FOUND


@quiz_blueprint.route("/<quiz_id>", methods=['GET'])
def get_quiz(quiz_id: str) -> jsonify:
    try:
        # Fetch data by id
        result = get_quiz_by_id(quiz_id)

        # Check if data exists
        if not result:
            return jsonify({"status": "error", "message":
                f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a quiz into the Firestore Database
#
@quiz_blueprint.route('/', methods=['POST'])
def add_quiz() -> jsonify:
    logging.info("\tRoutes Layer ==>	Creating new quiz loading...")
    try:
        data = request.get_json()

        # Extract and validate the fields
        title = data.get('title')
        description = data.get('description')
        teacher = data.get('teacher')
        questions = data.get('questions', [])

        if title is None or description is None or teacher is None:
            return jsonify({"status": "error",
                            "message": "Missing required fields title, description or teacher"}), HTTPStatus.BAD_REQUEST

        if not isinstance(questions, list):
            return jsonify({"status": "error",
                            "message": "Quiz needs a list of question."}), HTTPStatus.BAD_REQUEST

        # Convert questions into Question objects
        questions = [Question.from_dict(question) if isinstance(question, dict) else question for question in questions]
        quiz = Quiz(title, description, teacher, questions)

        # Call service function
        create_quiz(quiz)

        return jsonify({"status": "success",
                        "message": "Quiz created successfully."}), HTTPStatus.OK

    except StringLengthError as e:
        return jsonify({"status": "error",
                        "message": str(e)}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Update quiz route
#
@quiz_blueprint.route("/<quiz_id>", methods=['PUT'])
def update_quiz(quiz_id: str) -> jsonify:
    logging.info(f"\tRoutes Layer ==>	Updating quiz with id: {quiz_id} loading...")

    try:
        # Fetch updated data
        updated_data = request.get_json()

        # Call service function
        updated_quiz = update_quiz_data(updated_data, quiz_id)

        if not updated_quiz:
            return jsonify({"status": "error",
                            "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND
        else:
            return jsonify(updated_quiz), HTTPStatus.OK
    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Delete quiz route
#
@quiz_blueprint.route("/<quiz_id>", methods=['DELETE'])
def delete_quiz(quiz_id: str) -> jsonify:
    logging.info("\tRoutes Layer ==>	Deleting quiz loading...")
    try:
        # Call service function
        quiz = delete_quiz_by_id(quiz_id)

        if not quiz:
            return jsonify({"status": "error",
                            "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND
        else:
            return jsonify(quiz), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
