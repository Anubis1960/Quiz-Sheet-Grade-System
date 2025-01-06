from src.database import db
from src.models.quiz import Quiz
from src.services.student_service import get_student_by_unique_id
from src.util.mail_gen import send_email
from src.util.quiz_solver.bubble_solver import solve_quiz
from src.util.quiz_solver.process_quiz import parser

COLLECTION_NAME = 'quizzes'
MAX_QUESTION_LENGTH = 250
MAX_ANSWER_LENGTH = 100


#
#   Retrieve all quizzes
#
def get_quizzes_data() -> list[Quiz]:
    quizzes_data = db.collection(COLLECTION_NAME).stream()
    quizzes_list = [quiz.to_dict() for quiz in quizzes_data]
    return quizzes_list


#
# 	Retrieve quiz by id
# 	
def get_quiz_by_id(quiz_id: str) -> dict:
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()

    if not quiz_snapshot.exists:
        return {}

    return quiz_snapshot.to_dict()


#
#   Add
#
def create_quiz(quiz: Quiz) -> dict:
    for q in quiz.questions:
        if len(q.text) > MAX_QUESTION_LENGTH:
            return {"error": f"Question text exceeds {MAX_QUESTION_LENGTH} characters."}

        for option in q.options:
            if len(option) > MAX_ANSWER_LENGTH:
                return {"error": f"Option text exceeds {MAX_ANSWER_LENGTH} characters."}

    try:
        db.collection(COLLECTION_NAME).add(quiz.to_dict())
        return quiz.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


#
#	Update
#
def update_quiz_data(updated_data: dict, quiz_id: str) -> dict:
    try:
        quiz_ref = db.collection(COLLECTION_NAME).document(quiz_id)

        quiz_snapshot = quiz_ref.get()
        if not quiz_snapshot.exists:
            return {"error": f"No data found for id: {quiz_id}"}

        quiz_ref.update(updated_data)
        return updated_data

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


#
#	Delete
#
def delete_quiz_by_id(quiz_id: str) -> dict:
    try:
        quiz_ref = db.collection(COLLECTION_NAME).document(quiz_id)
        quiz = quiz_ref.get()
        if not quiz.exists:
            return {"error": f"No data found for id: {quiz_id}"}
        quiz_ref.delete()
        return quiz.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def grade_quiz(img):
    bubble_sheet, student_id, quiz_id = parser(img)
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        return "Quiz not found"
    correct_answers = [q['correct_answers'] for q in quiz['questions']]
    ans, score = solve_quiz(bubble_sheet, correct_answers)
    email = get_student_by_unique_id(student_id)[0]['email']
    send_email("Quiz Results", str(score), email)
    return score

