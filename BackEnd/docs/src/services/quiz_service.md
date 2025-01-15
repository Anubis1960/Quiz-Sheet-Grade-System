Module src.services.quiz_service
================================

Functions
---------

`create_quiz(quiz: src.models.quiz.Quiz) ‑> dict`
:   Adds a new quiz to the database.
    
    Args:
        quiz (Quiz): The quiz object to be added.
    
    Returns:
        dict: A dictionary containing the created quiz details or an error message if validation fails.

`delete_quiz_by_id(quiz_id: str) ‑> dict`
:   Deletes a quiz by its ID.
    
    Args:
        quiz_id (str): The unique ID of the quiz to be deleted.
    
    Returns:
        dict: A dictionary containing the deleted quiz details or an error message if the quiz was not found.

`get_quiz_by_id(quiz_id: str) ‑> dict`
:   Retrieves a specific quiz by its ID.
    
    Args:
        quiz_id (str): The unique ID of the quiz to fetch.
    
    Returns:
        dict: A dictionary containing the quiz details (title, description, questions), or an empty dictionary
        if not found.

`get_quizzes_by_teacher_id(teacher_id: str) ‑> list[dict]`
:   Retrieves all quizzes created by a specific teacher.
    
    Args:
        teacher_id (str): The unique ID of the teacher.
    
    Returns:
        list[dict]: A list of dictionaries containing quiz details (id, title, description, and questions).

`get_quizzes_data() ‑> list[dict]`
:   Fetches all quizzes from the database.
    
    Returns:
        list[dict]: A list of dictionaries containing quiz details (id, title, description, and questions).

`get_teacher_id(quiz_id: str) ‑> str`
:   Retrieves the teacher's ID associated with a specific quiz.
    
    Args:
        quiz_id (str): The unique ID of the quiz.
    
    Returns:
        str: The teacher's ID associated with the quiz.

`grade_quiz(img: cv2.Mat | numpy.ndarray) ‑> dict`
:   Grades a quiz based on a bubble sheet image.
    
    Args:
        img (MatLike): The image of the bubble sheet to be graded.
    
    Returns:
        dict: A dictionary containing the student's score and a message, or an error message if something goes wrong.

`update_quiz_data(updated_data: dict, quiz_id: str) ‑> dict`
:   Updates an existing quiz's data.
    
    Args:
        updated_data (dict): A dictionary containing the updated quiz data.
        quiz_id (str): The unique ID of the quiz to be updated.
    
    Returns:
        dict: A dictionary containing the updated quiz details or an error message if validation fails.