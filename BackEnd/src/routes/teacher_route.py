from http import HTTPStatus
from flask import Blueprint, request, jsonify
from src.services.teacher_service import *
from src.models.teacher import Teacher
from src.util.encrypt import *

TEACHER_URL = '/api/teachers'
teacher_blueprint = Blueprint('teacher', __name__, url_prefix=TEACHER_URL)


@teacher_blueprint.route('/', methods=['GET'])
def get_teachers() -> jsonify:
    """
    Retrieves a list of all teachers from the database.

    This endpoint accepts a GET request and returns a list of teachers in JSON format.

    Returns:
        jsonify: A list of teachers in JSON format.
        HTTPStatus: 200 OK if successful.
    """
    teachers = get_teachers_data()
    return jsonify(teachers), HTTPStatus.OK


@teacher_blueprint.route('/<teacher_id>', methods=['GET'])
def get_teacher(teacher_id: str) -> jsonify:
    """
    Retrieves a specific teacher's data based on the provided teacher ID.

    Args:
        teacher_id (str): The ID of the teacher to retrieve.

    Returns:
        jsonify: The teacher's data in JSON format if found.
        HTTPStatus: 200 OK if successful, 404 NOT FOUND if no data found for the provided ID.
    """
    try:
        teacher = get_teacher_by_id(teacher_id)

        if teacher is {}:
            return jsonify({"status": "error", "message": f"No data found for id: {teacher_id}"}), HTTPStatus.NOT_FOUND

        return jsonify(teacher), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@teacher_blueprint.route('/', methods=['POST'])
def add_teacher() -> jsonify:
    """
    Adds a new teacher to the database.

    This endpoint accepts a POST request with the following JSON body:
    - `name`: The name of the teacher.
    - `email`: The email of the teacher.
    - `password`: The password for the teacher (will be encrypted before storing).

    Returns:
        jsonify: The newly created teacher data in JSON format.
        HTTPStatus: 201 CREATED if the teacher is successfully created, 400 BAD REQUEST if validation fails.
    """
    try:
        data = request.get_json()

        name = data['name']
        email = data['email']
        password = data['password']

        # Encrypt password
        encrypted_password = encrypt(password)

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


@teacher_blueprint.route('/<teacher_id>', methods=['PUT'])
def update_teacher(teacher_id: str) -> jsonify:
    """
    Updates the data of an existing teacher in the database.

    Args:
        teacher_id (str): The ID of the teacher to update.

    This endpoint accepts a PUT request with the following JSON body:
    - `name`: The updated name of the teacher.
    - `email`: The updated email of the teacher.
    - `password`: The updated password for the teacher (will be encrypted before storing).

    Returns:
        jsonify: The updated teacher data in JSON format.
        HTTPStatus: 200 OK if the teacher is successfully updated, 400 BAD REQUEST if validation fails.
    """
    try:
        data = request.get_json()

        name = data['name']
        email = data['email']
        password = data['password']

        # Encrypt password
        encrypted_password = encrypt(password)

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


@teacher_blueprint.route('/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id: str) -> jsonify:
    """
    Deletes a teacher from the database based on the provided teacher ID.

    Args:
        teacher_id (str): The ID of the teacher to delete.

    Returns:
        jsonify: The deleted teacher's data in JSON format.
        HTTPStatus: 200 OK if successfully deleted, 404 NOT FOUND if no teacher exists with the provided ID.
    """
    try:

        teacher = delete_teacher_by_id(teacher_id)
        if "error" in teacher:
            return jsonify({"status": "error", "message": teacher["error"]}), HTTPStatus.NOT_FOUND

        return jsonify(teacher), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@teacher_blueprint.route('/email/<email>', methods=['GET'])
def get_by_email(email: str) -> jsonify:
    """
    Retrieves a teacher's data based on the provided email.

    Args:
        email (str): The email of the teacher to retrieve.

    Returns:
        jsonify: The teacher's data in JSON format if found.
        HTTPStatus: 200 OK if the teacher is found, 404 NOT FOUND if no teacher exists with the provided email.
    """
    try:
        teacher = get_teacher_by_email(email)

        if teacher is {}:
            return jsonify({"status": "error", "message": f"No data found for email: {email}"}), HTTPStatus.NOT_FOUND

        return jsonify(teacher), HTTPStatus.OK

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
