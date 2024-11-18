from src.database import db
from src.entities.Quiz import Quiz

def create_quiz(quiz: Quiz):
    # Convert quiz to a dictionary
    quiz_data = quiz.to_dict()
    print("Quiz data:",quiz_data)

    try:
        # Add quiz to the Firestore Database
        _,quiz_ref = db.collection("quizzes").add(quiz_data)
        return {"message":f"Quizz with title {quiz.title} added with ID: {quiz_ref.id}"}
    except Exception as e:
        return {"error": str(e)}

