from http import HTTPStatus
from flask import Blueprint, request, jsonify
from src.services.student_service import *
import re

STUDENT_URL = '/api/students'
REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
student_blueprint = Blueprint('student', __name__, url_prefix=STUDENT_URL)


@student_blueprint.route("/", methods=['GET'])
def get_students() -> jsonify:
    """
    Retrieves a list of all students from the database.

    This endpoint accepts a GET request and returns a list of students in JSON format.

    Returns:
        jsonify: A list of students in JSON format.
        HTTPStatus: 200 OK if successful.
    """
    students = get_students_data()
    return jsonify(students), HTTPStatus.OK


@student_blueprint.route("/<student_id>", methods=['GET'])
def get_student(student_id: str) -> jsonify:
    """
    Retrieves a specific student's data based on the provided student ID.

    Args:
        student_id (str): The ID of the student to retrieve.

    Returns:
        jsonify: The student's data in JSON format if found.
        HTTPStatus: 200 OK if successful, 404 NOT FOUND if no data found for the provided ID.
    """
    try:
        student = get_student_by_id(student_id)
        if not student:
            return jsonify({"status": "error", "message": f"No data found for id: {student_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@student_blueprint.route("/", methods=['POST'])
def add_student() -> jsonify:
    """
    Adds a new student to the database.

    This endpoint accepts a POST request with the following JSON body:
    - `unique_id`: The unique identifier of the student.
    - `email`: The email of the student (must be valid format).

    Returns:
        jsonify: The newly created student's data in JSON format.
        HTTPStatus: 201 CREATED if the student is successfully created, 400 BAD REQUEST if validation fails.
    """
    try:
        data = request.get_json()
        unique_id = data['unique_id']
        email = data['email']

        # Validate email format using regex
        if not re.match(REGEX, email):
            return jsonify({"status": "error", "message": "Invalid email format."}), HTTPStatus.BAD_REQUEST

        student = create_student(Student(unique_id, email))

        # Check if student has an error key
        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(student), HTTPStatus.CREATED

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@student_blueprint.route("/<student_id>", methods=['PUT'])
def update_student(student_id: str) -> jsonify:
    """
    Updates the data of an existing student in the database.

    Args:
        student_id (str): The ID of the student to update.

    This endpoint accepts a PUT request with the following JSON body:
    - `unique_id`: The updated unique identifier of the student.
    - `email`: The updated email of the student (must be valid format).

    Returns:
        jsonify: The updated student's data in JSON format.
        HTTPStatus: 200 OK if successful, 400 BAD REQUEST if validation fails.
    """
    try:
        data = request.get_json()

        # Extract data
        unique_id = data['unique_id']
        email = data['email']

        # Validate email format
        if not re.match(REGEX, email):
            return jsonify({"status": "error", "message": "Invalid email format."}), HTTPStatus.BAD_REQUEST

        student = update_student_data(student_id, Student(unique_id, email))

        # Check if student has an error key
        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.BAD_REQUEST

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@student_blueprint.route("/<student_id>", methods=['DELETE'])
def delete_student(student_id: str) -> jsonify:
    """
    Deletes a student from the database based on the provided student ID.

    Args:
        student_id (str): The ID of the student to delete.

    Returns:
        jsonify: The deleted student's data in JSON format.
        HTTPStatus: 200 OK if successfully deleted, 404 NOT FOUND if no student exists with the provided ID.
    """
    try:
        student = delete_student_by_id(student_id)

        if "error" in student:
            return jsonify({"status": "error", "message": student["error"]}), HTTPStatus.NOT_FOUND

        return jsonify(student), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR