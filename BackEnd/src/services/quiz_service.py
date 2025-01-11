from cv2.typing import MatLike
from tensorflow.python.util.numpy_compat import np_array

from src.database import db
from src.models.quiz import Quiz
from src.models.quizDTO import QuizDTO
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
def get_quizzes_data() -> list[dict]:
    quizDTOs = [QuizDTO(quiz.id, quiz.to_dict()['title'], quiz.to_dict()['description'],
                        quiz.to_dict()['questions']).to_dict()
                for quiz in db.collection(COLLECTION_NAME).stream()]
    return quizDTOs


#
# 	Retrieve quiz by id
# 	
def get_quiz_by_id(quiz_id: str) -> dict:
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()

    if not quiz_snapshot.exists:
        return {}

    return QuizDTO(quiz_id, quiz_snapshot.get('title'), quiz_snapshot.get('description'),
                   quiz_snapshot.get('questions')).to_dict()


#
#   Add
#
def create_quiz(quiz: Quiz) -> dict:
    try:
        if len(quiz.title) == 0:
            return {"error": "Title cannot be empty"}
        if len(quiz.questions) == 0:
            return {"error": "Questions cannot be empty"}
        if len(quiz.questions) > 10:
            return {"error": f"Questions cannot exceed 10"}
        _, quiz_ref = db.collection(COLLECTION_NAME).add(quiz.to_dict())
        return QuizDTO(quiz_ref.id, quiz.title, quiz.description,
                       [question.to_dict() for question in quiz.questions]).to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


#
#	Update
#
def update_quiz_data(updated_data: dict, quiz_id: str) -> dict:
    try:
        if len(updated_data['title']) == 0:
            return {"error": "Title cannot be empty"}
        if len(updated_data['questions']) == 0:\
            return {"error": "Questions cannot be empty"}
        if len(updated_data['questions']) > 10:
            return {"error": f"Questions cannot exceed 10"}
        quiz_ref = db.collection(COLLECTION_NAME).document(quiz_id)

        quiz_snapshot = quiz_ref.get()
        if not quiz_snapshot.exists:
            return {"error": f"No data found for id: {quiz_id}"}

        quiz_ref.update(updated_data)
        return QuizDTO(quiz_id, updated_data['title'], updated_data['description'], updated_data['questions']).to_dict()

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
        return QuizDTO(quiz_id, quiz['title'], quiz['description'], quiz['questions']).to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def grade_quiz(img: MatLike) -> dict:
    try:
        resp = {}
        bubble_sheet, student_id, quiz_id = parser(img)
        print(student_id)
        print(quiz_id)

        if bubble_sheet is None:
            return {"error": "No bubble sheet found"}

        if quiz_id == "":
            return {"error": "Quiz not found"}

        quiz = get_quiz_by_id(quiz_id)

        if not quiz:
            return {"error": "Quiz not found"}

        correct_answers = [q['correct_answers'] for q in quiz['questions']]
        print(correct_answers)

        ans, score = solve_quiz(bubble_sheet, correct_answers)
        if student_id != "":
            students = get_student_by_unique_id(student_id)
            if len(students) != 0:
                email = students[0]['email']
                send_email("Quiz Results", str(score), email)
        else:
            resp["message"] = "Student ID not found"
        resp["score"] = score
        return resp
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def get_teacher_id(quiz_id: str) -> str:
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()
    print(quiz_snapshot.to_dict())
    return quiz_snapshot.get('teacher')


def get_quizzes_by_teacher_id(teacher_id: str) -> list[dict]:
    quizDTOs = [QuizDTO(quiz.id, quiz.to_dict()['title'], quiz.to_dict()['description'],
                        quiz.to_dict()['questions']).to_dict()
                for quiz in db.collection(COLLECTION_NAME).where('teacher', '==', teacher_id).stream()]
    return quizDTOs
