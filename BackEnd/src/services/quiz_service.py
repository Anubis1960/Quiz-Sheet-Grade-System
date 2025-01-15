from cv2.typing import MatLike
from src.database import db
from src.models.quiz import Quiz
from src.models.quizDTO import QuizDTO
from src.services.student_service import get_student_by_unique_id
from src.util.mail_gen import send_email
from src.util.quiz_solver.bubble_solver import solve_quiz
from src.util.quiz_solver.process_quiz import parser

COLLECTION_NAME = 'quizzes'
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 200


def get_quizzes_data() -> list[dict]:
    """
    Fetches all quizzes from the database.

    Returns:
        list[dict]: A list of dictionaries containing quiz details (id, title, description, and questions).
    """
    quizDTOs = [QuizDTO(quiz.id, quiz.to_dict()['title'], quiz.to_dict()['description'],
                        quiz.to_dict()['questions']).to_dict()
                for quiz in db.collection(COLLECTION_NAME).stream()]
    return quizDTOs


def get_quiz_by_id(quiz_id: str) -> dict:
    """
    Retrieves a specific quiz by its ID.

    Args:
        quiz_id (str): The unique ID of the quiz to fetch.

    Returns:
        dict: A dictionary containing the quiz details (title, description, questions), or an empty dictionary
        if not found.
    """
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()

    if not quiz_snapshot.exists:
        return {}

    return QuizDTO(quiz_id, quiz_snapshot.get('title'), quiz_snapshot.get('description'),
                   quiz_snapshot.get('questions')).to_dict()


def create_quiz(quiz: Quiz) -> dict:
    """
    Adds a new quiz to the database.

    Args:
        quiz (Quiz): The quiz object to be added.

    Returns:
        dict: A dictionary containing the created quiz details or an error message if validation fails.
    """
    try:
        if len(quiz.title) == 0:
            return {"error": "Title cannot be empty"}
        if len(quiz.questions) == 0:
            return {"error": "Questions cannot be empty"}
        # if len(quiz.questions) > 10:
        #     return {"error": f"Questions cannot exceed 10"}
        if len(quiz.title) > MAX_TITLE_LENGTH:
            return {"error": f"Title cannot exceed {MAX_TITLE_LENGTH}"}
        if len(quiz.description) > MAX_DESCRIPTION_LENGTH:
            return {"error": f"Description cannot exceed {MAX_DESCRIPTION_LENGTH}"}
        _, quiz_ref = db.collection(COLLECTION_NAME).add(quiz.to_dict())
        return QuizDTO(quiz_ref.id, quiz.title, quiz.description,
                       [question.to_dict() for question in quiz.questions]).to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def update_quiz_data(updated_data: dict, quiz_id: str) -> dict:
    """
    Updates an existing quiz's data.

    Args:
        updated_data (dict): A dictionary containing the updated quiz data.
        quiz_id (str): The unique ID of the quiz to be updated.

    Returns:
        dict: A dictionary containing the updated quiz details or an error message if validation fails.
    """
    try:
        if len(updated_data['title']) == 0:
            return {"error": "Title cannot be empty"}
        if len(updated_data['questions']) == 0:
            return {"error": "Questions cannot be empty"}
        # if len(updated_data['questions']) > 10:
        #     return {"error": f"Questions cannot exceed 10"}
        if len(updated_data['title']) > MAX_TITLE_LENGTH:
            return {"error": f"Title cannot exceed {MAX_TITLE_LENGTH}"}
        if len(updated_data['description']) > MAX_DESCRIPTION_LENGTH:
            return {"error": f"Description cannot exceed {MAX_DESCRIPTION_LENGTH}"}
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
# Delete quiz by ID
#
def delete_quiz_by_id(quiz_id: str) -> dict:
    """
    Deletes a quiz by its ID.

    Args:
        quiz_id (str): The unique ID of the quiz to be deleted.

    Returns:
        dict: A dictionary containing the deleted quiz details or an error message if the quiz was not found.
    """
    try:
        quiz_ref = db.collection(COLLECTION_NAME).document(quiz_id)
        quiz_snapshot = quiz_ref.get()

        if not quiz_snapshot.exists:
            return {"error": f"No data found for id: {quiz_id}"}

        quiz_data = quiz_snapshot.to_dict()

        quiz_ref.delete()

        return QuizDTO(quiz_id, quiz_data['title'], quiz_data['description'], quiz_data['questions']).to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def grade_quiz(img: MatLike) -> dict:
    """
    Grades a quiz based on a bubble sheet image.

    Args:
        img (MatLike): The image of the bubble sheet to be graded.

    Returns:
        dict: A dictionary containing the student's score and a message, or an error message if something goes wrong.
    """
    try:
        resp = {}
        bubble_sheet, student_id, quiz_id = parser(img)

        if bubble_sheet is None:
            return {"error": "No bubble sheet found"}

        if quiz_id == "":
            return {"error": "Quiz not found"}

        quiz = get_quiz_by_id(quiz_id)

        if not quiz:
            return {"error": "Quiz not found"}

        correct_answers = [q['correct_answers'] for q in quiz['questions']]

        idx = 0
        total_correct = 0
        for sheet in bubble_sheet:

            ans, num_correct = solve_quiz(sheet, correct_answers[idx:min(idx + 10, len(correct_answers))])
            idx += 10
            total_correct += num_correct

        score = (total_correct / len(correct_answers)) * 100
        if student_id != "":
            students = get_student_by_unique_id(student_id)
            if len(students) != 0:
                email = students[0]['email']
                message = f"Congratulations! You scored {score} on the {quiz['title']} quiz"
                send_email("Quiz Results", message, email)
            else:
                resp["message"] = "Student ID not found"
        else:
            resp["message"] = "Student ID not found"
        resp["score"] = score
        return resp
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def get_teacher_id(quiz_id: str) -> str:
    """
    Retrieves the teacher's ID associated with a specific quiz.

    Args:
        quiz_id (str): The unique ID of the quiz.

    Returns:
        str: The teacher's ID associated with the quiz.
    """
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()
    return quiz_snapshot.get('teacher')


def get_quizzes_by_teacher_id(teacher_id: str) -> list[dict]:
    """
    Retrieves all quizzes created by a specific teacher.

    Args:
        teacher_id (str): The unique ID of the teacher.

    Returns:
        list[dict]: A list of dictionaries containing quiz details (id, title, description, and questions).
    """
    quizDTOs = [
        QuizDTO(
            quiz.id,
            quiz.to_dict()['title'],
            quiz.to_dict()['description'],
            quiz.to_dict()['questions']
        ).to_dict()
        for quiz in db.collection(COLLECTION_NAME)
        .where('teacher', '==', teacher_id)
        .stream()
    ]
    return quizDTOs
