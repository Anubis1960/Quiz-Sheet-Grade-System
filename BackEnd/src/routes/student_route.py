from http import HTTPStatus

from flask import Blueprint, request, jsonify

from src.services.student_service import *

#
#	Define URL for students
#
STUDENT_URL = '/api/students'
#
#	Students Blueprint
#
student_blueprint = Blueprint('student', __name__, url_prefix=STUDENT_URL)


#
#	Route to get all students from the db
#
@student_blueprint.route("/", methods=['GET'])
def get_students() -> jsonify:
    students = get_students_data()
    return jsonify(students), HTTPStatus.OK


# 
# 	Route to get a student from the db
#     
@student_blueprint.route("/<student_id>", methods=['GET'])
def get_student(student_id: str) -> jsonify:
    try:
        student = get_student_by_id(student_id)
        if not student:
            return jsonify({"status": "error", "message": f"No data found for id: {student_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a student into the Firestore Database
#
@student_blueprint.route("/", methods=['POST'])
def add_student() -> jsonify:
    try:
        data = request.get_json()
        unique_id = data['unique_id']
        email = data['email']

        student = create_student(Student(unique_id, email))

        # Check if student has an error key
        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(student), HTTPStatus.CREATED

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#    Route to update a student in the Firestore Database
#
@student_blueprint.route("/<student_id>", methods=['PUT'])
def update_student(student_id: str) -> jsonify:
    try:
        data = request.get_json()

        # Extract data
        unique_id = data['unique_id']
        email = data['email']

        student = update_student_data(student_id, Student(unique_id, email))

        # Check if student has an error key
        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to delete a student from the Firestore Database
#
@student_blueprint.route("/<student_id>", methods=['DELETE'])
def delete_student(student_id: str) -> jsonify:
    try:
        student = delete_student_by_id(student_id)

        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.NOT_FOUND

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
