import logging
from http import HTTPStatus
from flask import Blueprint,request,jsonify
from src.services.teacher_service import *
from src.entities.Teacher import Teacher

#
#	Define URL for teachers
#
TEACHER_URL = '/api/teachers'
#
#   Teacher Blueprint
#
teacher_blueprint = Blueprint('teacher',__name__, url_prefix= TEACHER_URL)

#
#   Retrieve teachers data
#
@teacher_blueprint.route('/', methods = ['GET'])
def get_teachers() -> jsonify:
	logging.info("\tRoutes Layer ==>	Requesting teachers list.")

	# Fetch teachers data from db
	teachers_data = get_teachers_data()

	if teachers_data is None:
		return jsonify({"status: " : "error",
						"message": "No teachers data."}), HTTPStatus.NOT_FOUND
	
	return jsonify({"teachers": teachers_data}), HTTPStatus.OK
	
	

#
#	Route to get a teacher from the Firestore Database
#
@teacher_blueprint.route('/<teacher_id>',methods = ['GET'])
def get_teacher(teacher_id: str) -> jsonify:
	logging.info("\tRoutes Layer ==>	Requesting teacher by id loading...")

	try:
		result = get_teacher_by_id(teacher_id)

		# Verify if result is a dictionary and contains an 'error' key
		if isinstance(result,dict) and "error" in result:
			return jsonify({"status": "error", 
							"message": f"No data found for id: {teacher_id}"}), HTTPStatus.NOT_FOUND

		return jsonify(result.to_dict()), HTTPStatus.OK

	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Route to add a teacher into the Firestore Database
#
@teacher_blueprint.route('/',methods = ['POST'])
def add_teacher() -> jsonify:
	logging.info("\tRoutes Layer ==>	Creating new teacher loading...")
	try:
		# Retrieve JSON 
		data = request.get_json()

		# Retrieve JSON data
		name = data['name']
		email = data['email']
		password = data['password']

		# Create object
		teacher = Teacher(name, email, password)
		result = create_teacher(teacher)

		return jsonify({"status": "success", 
						"message": "Teacher added successfully."}), HTTPStatus.OK
	
	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	

#
#	Route to delete a teacher from Firestore Database
#
@teacher_blueprint.route('/<teacher_id>',methods = ['DELETE'])
def delete_teacher(teacher_id: str) -> jsonify:
	logging.info("\tRoutes Layer ==>	Deleting teacher loading...")
	try:
		teacher_to_be_deleted = delete_teacher_by_id(teacher_id)

		# Verify received data
		if isinstance(teacher_to_be_deleted,dict) and "error" in teacher_to_be_deleted:
			return jsonify(teacher_to_be_deleted), HTTPStatus.NOT_FOUND
		
		return jsonify({"status": "success", 
						"message": "Teacher deleted successfully."}), HTTPStatus.OK

	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
