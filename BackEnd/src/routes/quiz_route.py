import logging
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from src.entities.Quiz import Quiz
from src.services.quiz_service import *
from src.entities.Question import Question
from src.exceptions.NoDataFoundError import NoDataFoundError
from src.exceptions.StringLengthError  import StringLengthError

#
#	Define URL for quizzes
#
QUIZ_URL = '/api/quizzes'
#
#   Quiz Blueprint
#
quiz_blueprint = Blueprint('quiz',__name__, url_prefix= QUIZ_URL)

#
#	Route to display list of quizzes
#
@quiz_blueprint.route('/', methods = ['GET'])
def get_quizzes() -> jsonify:
	logging.info("\tRoutes Layer ==>	Requesting quizzes list loading...")

	try:
		# Retrieve quizzes
		quizzes_data = get_quizzes_data()

		# Verify if data exists
		if quizzes_data is None:
			return jsonify({"status:": "error",
							"message": "No quizzes available"}), HTTPStatus.NOT_FOUND
		
		return jsonify({"quizzes": quizzes_data}), HTTPStatus.OK

	except NoDataFoundError as e:
		return jsonify({"status": "error", 
						"message": str(e)}), HTTPStatus.NOT_FOUND


#
#	Route to add a quiz into the Firestore Database
#
@quiz_blueprint.route('/',methods = ['POST'])
def add_quiz() -> jsonify:
	logging.info("\tRoutes Layer ==>	Creating new quiz loading...")
	try:
		data = request.get_json()

		# Extract and validate the fields
		title = data.get('title')
		description = data.get('description')
		teacher = data.get('teacher')
		questions = data.get('questions',[])	

		if title is None or description is None or teacher is None:
			return jsonify({"status": "error",
							"message": "Missing required fields title, description or teacher"}), HTTPStatus.BAD_REQUEST

		if not isinstance(questions,list):
			return jsonify({"status": "error",
				   			"message":"Quiz needs a list of question."}), HTTPStatus.BAD_REQUEST
		
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
@quiz_blueprint.route("/<quiz_id>", methods = ['PUT'])
def update_quiz(quiz_id: str) -> jsonify:
	logging.info(f"\tRoutes Layer ==>	Updating quiz with id: {quiz_id} loading...")

	try:
		# Fetch updated data 
		updated_data = request.get_json()
		logging.debug(f"Display JSON data: {updated_data}")
		
		# Call service function
		update_quiz_data(updated_data, quiz_id)

		return jsonify({"status": "success", 
						"message": "Quiz updated successfully."}), HTTPStatus.OK
	
	#
	#	Except Handlings
	#
	except LookupError as e:
		logging.error(f"\tRoutes Layer ==> Error: {str(e)}")
		return jsonify({
			"status": "error",
			"message": str(e)
		}), HTTPStatus.NOT_FOUND
	
	except Exception as e:
			# Catch unexpected errors
			return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
	
#
#	Delete quiz route
#
@quiz_blueprint.route("/<quiz_id>", methods = ['DELETE'])
def delete_quiz(quiz_id: str) -> jsonify:
		logging.info("\tRoutes Layer ==>	Deleting quiz loading...")
		try:
			# Call service function
			delete_quiz_by_id(quiz_id)

			return jsonify({"status": "success", 
						"message": "Quiz deleted successfully."}), HTTPStatus.OK
		
		except Exception as e:
			# Catch unexpected errors
			return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR