from flask import Blueprint, request, jsonify
from src.entities.Quiz import Quiz
from src.services.quiz_service import create_quiz
from src.entities.Question import Question

#
#	Define URL for quizzes
#
QUIZ_URL = '/api/quizzes'
#
#   Quiz Blueprint
#
quiz_blueprint = Blueprint('quiz',__name__, url_prefix= QUIZ_URL)

#
# Route to add a quiz into the Firestore Database
#
@quiz_blueprint.route('/',methods = ['POST'])
def add_quiz():
	try:
		data = request.get_json()
		if not data:
			return jsonify({"error":"No data provided"}), 400
		print("Incoming data",data)

		# Extract and validate the fields
		title = data.get('title')
		description = data.get('description')
		teacher = data.get('teacher')
		questions = data.get('questions',[])
		
		if not title or description or teacher:
			return jsonify({"error":"Missing requierd fields title,description or teacher"})

		if not isinstance(questions,list):
			return jsonify({"error":"Questions must be a list"}), 400
		
		# Convert questions into Question objects 
		questions = [Question.from_dict(q) if isinstance(q, dict) else q for q in questions]
		quiz = Quiz(title = title,description = description,teacher = teacher,questions = questions)
		result = create_quiz(quiz)
		print("Result from create_quiz():",result)

		if "error" in result:
			return jsonify(result), 400

		return jsonify(result), 200
	except Exception as e:
		return {"error": str(e)}