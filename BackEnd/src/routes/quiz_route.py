from http import HTTPStatus

import cv2
import numpy as np
from flask import Blueprint, request, jsonify
from flask import send_file
from src.util.pdf_gen import generate_pdf
from src.models.question import Question
from src.services.quiz_service import *
from src.services.teacher_service import get_teacher_by_id

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
			return jsonify({"status": "error", "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

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
		questions = data.get('questions', [])
		teacher_id = data.get('teacher')

		quiz = create_quiz(
			Quiz(title, description, teacher_id, [Question.from_dict(question) for question in questions]))

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


@quiz_blueprint.route("/pdf/<quiz_id>", methods=['GET'])
def export_pdf(quiz_id: str) -> jsonify:
	try:
		quiz = get_quiz_by_id(quiz_id)

		if not quiz:
			return jsonify({"status": "error", "message": f"No data found for id: {quiz_id}"}), HTTPStatus.NOT_FOUND

		teacher_id = get_by_teacher_id(quiz['id'])
		if not teacher_id:
			return jsonify({"status": "error", "message": f"No teacher found for quiz id: {quiz_id}"}), HTTPStatus.NOT_FOUND

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
def grade():
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
	try:
		quizzes = get_quizzes_by_teacher_id(teacher_id)
		return jsonify(quizzes), HTTPStatus.OK
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
