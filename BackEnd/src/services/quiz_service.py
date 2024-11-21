import logging

from src.database import db
from src.exceptions.StringLengthError import StringLengthError
from src.models.quiz import Quiz

COLLECTION_NAME = 'quizzes'
MAX_QUESTION_LENGTH = 250
MAX_ANSWER_LENGTH = 100


#
#   Retrieve all quizzes
#
def get_quizzes_data() -> list[Quiz]:
    logging.info("\tService Layer ==>	Retrieve quizzes loading...")

    # Fetch data from databse
    quizzes_data = db.collection(COLLECTION_NAME).stream()

    # Create list of quizzes
    quizzes_list = [quiz.to_dict() for quiz in quizzes_data]

    logging.info("\tService Layer ==>	Successfully retrieved quizzes list.")
    return quizzes_list


#
# 	Retrieve quiz by id
# 	
def get_quiz_by_id(quiz_id: str) -> dict:
    logging.info("\tService Layer ==>	Retrieve quiz by id loading...")

    # Fetch data based on id
    quiz_snapshot = db.collection(COLLECTION_NAME).document(quiz_id).get()
    logging.debug(f"Retrieved quiz_data: {quiz_snapshot}")

    # Check if data exists
    if not quiz_snapshot.exists:
        logging.warning(f"\tService Layer ==>	No data found for quiz with id: {quiz_id}")
        return {}

    logging.info(f"\tService Layer ==>	Successfully retrieved quiz with id: {quiz_id}")
    return quiz_snapshot.to_dict()


####################################
#
#   CRUD Operations
#
####################################

#
#   Add
#
def create_quiz(quiz: Quiz) -> None:
    logging.info("\tRoutes Layer ==>	Creating new quiz loading...")
    # Convert quiz to a dictionary
    quiz_data = quiz.to_dict()

    # Validate quiz questions length
    for idx, question in enumerate(quiz_data['questions'], start=1):

        if len(question['text']) >= MAX_QUESTION_LENGTH:
            logging.warning(f"Question: {idx} exceeds the maximum length of {MAX_QUESTION_LENGTH} characters.")
            raise StringLengthError(f"Question {idx} exceeds the maximum length of {MAX_QUESTION_LENGTH} characters.")

        # Validate question answers length
        for i, option in enumerate(question['options'], start=1):

            if len(option) >= MAX_QUESTION_LENGTH:
                logging.warning(f"Option: {i} exceeds the maximum length of {MAX_QUESTION_LENGTH} characters.")
                raise StringLengthError(f"Option {i} exceeds the maximum length of {MAX_QUESTION_LENGTH} characters.")

    # Add quiz to the Firestore Database
    db.collection("quizzes").add(quiz_data)
    logging.info("\tService Layer ==>	Successfully created quiz.")


#
#	Update
#
def update_quiz_data(updated_data: dict, quiz_id: str) -> dict | None:
    logging.info("\tService Layer ==>	Updating quiz loading...")

    # Retrieve data of quiz that gets updated
    quiz_data = get_quiz_by_id(quiz_id)

    if not quiz_data:
        return None

    # Update fields
    for key in ['title', 'description', 'teacher']:
        # Verify which field gets update
        if key in updated_data:
            quiz_data[key] = updated_data[key]



    '''
    	First, check if there are any new questions in the update data. 
    For each question, ensure that all its properties—such as 
    text, options, and correct_answers—are updated accordingly. 
    	Additionally, if there are new questions in the update data 
    that do not already exist in the quiz, make sure to add them 
    to the quiz object, keeping the quiz data properly updated and 
    consistent.
    '''

    if 'questions' in updated_data:
        logging.debug("New questions data found inside JSON.")
        for updated_question in updated_data['questions']:

            # Variable that help us to track update question
            found = False
            for question in quiz_data['questions']:

                # Update question text
                if question['text'] == updated_question['text']:
                    # Update details of question
                    question.update(updated_question)

                    # Mark that question was found
                    found = True
                    break

            if not found:
                # Case where question wasn't found, so we add it
                quiz_data['questions'].append(updated_question)

    # Retrieve reference of quiz that needs to be updated
    quiz_ref = db.collection(COLLECTION_NAME).document(quiz_id)

    # Update quiz in Firestore
    quiz_ref.set(quiz_data)
    logging.info("\tService Layer ==>	Successfully updated quiz.")
    return quiz_data


#
#	Delete
#
def delete_quiz_by_id(quiz_id: str) -> dict:
    # Verify if quiz exists using id
    print(f"Deleting quiz with id: {quiz_id}")
    quiz = get_quiz_by_id(quiz_id)

    if not quiz:
        return {}

    # Retrieve document reference and delete it
    db.collection(COLLECTION_NAME).document(quiz_id).delete()
    logging.info("\tService Layer ==>	Quiz deleted successfully.")
    return quiz
