from http import HTTPStatus
from flask import Blueprint, request, jsonify
from src.services.teacher_service import *
from src.models.teacher import Teacher
from src.util.encrypt import *

#
#	Define URL for teachers
#
TEACHER_URL = '/api/teachers'
#
#   Teacher Blueprint
#
teacher_blueprint = Blueprint('teacher', __name__, url_prefix=TEACHER_URL)


#
#   Retrieve teachers data
#
@teacher_blueprint.route('/', methods=['GET'])
def get_teachers() -> jsonify:
	teachers = get_teachers_data()
	return jsonify(teachers), HTTPStatus.OK


#
#	Route to get a teacher from the Firestore Database
#
@teacher_blueprint.route('/<teacher_id>', methods=['GET'])
def get_teacher(teacher_id: str) -> jsonify:
	try:
		teacher = get_teacher_by_id(teacher_id)

		if teacher is {}:
			return jsonify({"status": "error", "message": f"No data found for id: {teacher_id}"}), HTTPStatus.NOT_FOUND

		return jsonify(teacher), HTTPStatus.OK

	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a teacher into the Firestore Database
#
@teacher_blueprint.route('/', methods=['POST'])
def add_teacher() -> jsonify:
	try:
		data = request.get_json()

		name = data['name']
		email = data['email']
		password = data['password']

		# Encrypt password
		encrypted_password = sha256(password)

		teacher = create_teacher(Teacher(name, email, encrypted_password))

		if "error" in teacher:
			return jsonify({"status": "error", "message": teacher["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(teacher), HTTPStatus.CREATED

	except ValueError as e:
		return jsonify({
			"status": "error",
			"message": str(e)
		}), HTTPStatus.BAD_REQUEST

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#    Route to update a teacher in the Firestore Database
#
@teacher_blueprint.route('/<teacher_id>', methods=['PUT'])
def update_teacher(teacher_id: str) -> jsonify:
	try:
		data = request.get_json()

		name = data['name']
		email = data['email']
		password = data['password']

		# Encrypt password
		encrypted_password = sha256(password)

		teacher = update_teacher_by_id(teacher_id, Teacher(name, email, encrypted_password))

		if "error" in teacher:
			return jsonify({"status": "error", "message": teacher["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(teacher), HTTPStatus.OK

	except ValueError as e:
		return jsonify({
			"status": "error",
			"message": str(e)
		}), HTTPStatus.BAD_REQUEST

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to delete a teacher from Firestore Database
#
@teacher_blueprint.route('/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id: str) -> jsonify:
	try:

		teacher = delete_teacher_by_id(teacher_id)
		if "error" in teacher:
			return jsonify({"status": "error", "message": teacher["error"]}), HTTPStatus.NOT_FOUND

		return jsonify(teacher), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@teacher_blueprint.route('/email/<email>', methods=['GET'])
def get_by_email(email: str) -> jsonify:
	try:
		teacher = get_teacher_by_email(email)

		if teacher is {}:
			return jsonify({"status": "error", "message": f"No data found for email: {email}"}), HTTPStatus.NOT_FOUND

		return jsonify(teacher), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
