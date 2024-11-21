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
#	Route to retrieve all students from the Firestore DB
#
@student_blueprint.route("/", methods=['GET'])
def get_students() -> jsonify:
    logging.info("\tRoutes Layer ==>	Requesting students list loading...")

    # Retrieve students data
    students_data = get_students_data()

    if students_data is []:
        return jsonify([]), HTTPStatus.NOT_FOUND

    return jsonify(students_data), HTTPStatus.OK


# 
# 	Route to get a student from the Firestore Database
#     
@student_blueprint.route("/<student_id>", methods=['GET'])
def get_student(student_id: str) -> jsonify:
    logging.info("\tRoutes Layer ==>	Requesting student by id loading...")
    try:
        # Fetch data by id
        result = get_student_by_id(student_id)

        # Check if data exists
        if not result:
            return jsonify({"status": "error", "message":
                f"No data found for id: {student_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(result.to_dict()), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a student into the Firestore Database
#
@student_blueprint.route("/", methods=['POST'])
def add_student() -> jsonify:
    logging.info("\tRoutes Layer ==>	Creating new student loading...")
    try:
        # Retrieve JSON
        data = request.get_json()

        # Retrieve JSON data
        unique_id = data['unique_id']
        email = data['email']

        # Create object
        student = Student(unique_id, email)

        # Send data to service layer function
        response = create_student(student)

        # Check for errors
        if response is "error":
            return jsonify({"status": "failure",
                            "error": response["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify({"status": "success",
                        "message": "Student added successfully."}), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to delete a student from the Firestore Database
#
@student_blueprint.route("/<student_id>", methods=['DELETE'])
def delete_student(student_id: str) -> jsonify:
    logging.info("\tRoutes Layer ==>	Deleting student loading...")
    try:
        student_to_be_deleted = delete_student_by_id(student_id)

        # Verify if result is a dictionary and contains an 'error' key
        if isinstance(student_to_be_deleted, dict) and "error" in student_to_be_deleted:
            return jsonify({"status": "error",
                            "message": f"No data found for id: {student_id}"}), HTTPStatus.NOT_FOUND

        return jsonify({"status": "success",
                        "message": "Student deleted successfully."}), HTTPStatus.OK

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR