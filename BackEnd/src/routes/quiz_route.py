from http import HTTPStatus

import cv2
import numpy as np
from flask import Blueprint, request, jsonify
from flask import send_file
from src.util.pdf_gen import generate_pdf
from src.models.question import Question
from src.services.quiz_service import *
from src.services.teacher_service import get_teacher_by_id

QUIZ_URL = '/api/quizzes'
quiz_blueprint = Blueprint('quiz', __name__, url_prefix=QUIZ_URL)


@quiz_blueprint.route('/', methods=['GET'])
def get_quizzes() -> jsonify:
    """
    Retrieve the list of all quizzes.

    This route returns a list of quizzes stored in the database.

    Returns:
        jsonify: A list of quizzes with a 200 OK status.
    """
    quizzes_data = get_quizzes_data()
    return jsonify(quizzes_data), HTTPStatus.OK


@quiz_blueprint.route("/<quiz_id>", methods=['GET'])
def get_quiz(quiz_id: str) -> jsonify:
    """
    Retrieve a specific quiz by its ID.

    This route retrieves a quiz based on the provided `quiz_id`. If no quiz is found, it returns a 404 error.

    Args:
        quiz_id (str): The ID of the quiz to retrieve.

    Returns:
        jsonify: The quiz data with a 200 OK status, or an error message with a 404 status if not found.
    """
    try:
        quiz = get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({"status": "error", "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route('/', methods=['POST'])
def add_quiz() -> jsonify:
    """
    Add a new quiz to the database.

    This route accepts the quiz data (title, description, questions, and teacher ID) and creates a new quiz record.

    Returns:
        jsonify: The created quiz data with a 201 CREATED status, or an error message with a 400 BAD REQUEST status.
    """
    try:
        data = request.get_json()

        title = data.get('title')
        description = data.get('description')
        questions = data.get('questions', [])
        teacher_id = data.get('teacher')

        quiz = create_quiz(
            Quiz(title, description, teacher_id, [Question.from_dict(question) for question in questions]))

        if "error" in quiz:
            return jsonify({"status": "error", "message": quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(quiz), HTTPStatus.CREATED

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/<quiz_id>", methods=['PUT'])
def update_quiz(quiz_id: str) -> jsonify:
    """
    Update an existing quiz.

    This route allows updating quiz details based on the `quiz_id`. The provided data will overwrite the existing quiz.

    Args:
        quiz_id (str): The ID of the quiz to update.

    Returns:
        jsonify: The updated quiz data with a 200 OK status, or an error message with a 400 BAD REQUEST status.
    """
    try:
        updated_data = request.get_json()
        updated_quiz = update_quiz_data(updated_data, quiz_id)

        if "error" in updated_quiz:
            return jsonify({"status": "error", "message": updated_quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(updated_quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/<quiz_id>", methods=['DELETE'])
def delete_quiz(quiz_id: str) -> jsonify:
    """
    Delete a specific quiz by its ID.

    This route deletes a quiz based on the provided `quiz_id`. If the quiz is not found, a 400 error is returned.

    Args:
        quiz_id (str): The ID of the quiz to delete.

    Returns:
        jsonify: The deletion result with a 200 OK status, or an error message with a 400 BAD REQUEST status.
    """
    try:
        quiz = delete_quiz_by_id(quiz_id)

        if "error" in quiz:
            return jsonify({"status": "error", "message": quiz["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(quiz), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/pdf/<quiz_id>", methods=['GET'])
def export_pdf(quiz_id: str) -> jsonify:
    """
    Export a quiz to a PDF file.

    This route generates a PDF of the specified quiz and its associated teacher. The PDF is returned as an attachment.

    Args:
        quiz_id (str): The ID of the quiz to export to PDF.

    Returns:
        send_file: The generated PDF file as a downloadable attachment, or an error message with a 400 status if
        not found.
    """
    try:
        quiz = get_quiz_by_id(quiz_id)

        if not quiz:
            return jsonify({"status": "error", "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

        teacher_id = get_teacher_id(quiz['id'])
        if not teacher_id:
            return (jsonify(
                {"status": "error", "message": f"No teacher found for quiz id: {quiz_id}"}), HTTPStatus.NOT_FOUND)

        teacher = get_teacher_by_id(teacher_id)

        pdf_buffer = generate_pdf(quiz_id, quiz, teacher['name'])

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{quiz_id}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/grade", methods=['POST'])
def grade() -> jsonify:
    """
    Grade a quiz based on an image submission.

    This route accepts an image containing the completed quiz, processes it, and returns the grading results.

    Returns:
        jsonify: The grading results with a 200 OK status, or an error message with a 400 BAD REQUEST status.
    """
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"}), HTTPStatus.BAD_REQUEST

        file = request.files['image']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), HTTPStatus.BAD_REQUEST

        b_file = file.read()

        nparr = np.frombuffer(b_file, np.uint8)

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"status": "error", "message": "Failed to decode the image"}), HTTPStatus.BAD_REQUEST

        # Your image processing function
        gr = grade_quiz(img)

        if "error" in gr:
            return jsonify({"status": "error", "message": gr["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(gr), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR


@quiz_blueprint.route("/all/<teacher_id>", methods=['GET'])
def get_by_teacher_id(teacher_id: str) -> jsonify:
    """
    Retrieve all quizzes created by a specific teacher.

    This route returns a list of quizzes associated with the given teacher ID.

    Args:
        teacher_id (str): The ID of the teacher whose quizzes are to be retrieved.

    Returns:
        jsonify: A list of quizzes with a 200 OK status, or an error message with a 400 BAD REQUEST status.
    """
    try:
        quizzes = get_quizzes_by_teacher_id(teacher_id)
        return jsonify(quizzes), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR