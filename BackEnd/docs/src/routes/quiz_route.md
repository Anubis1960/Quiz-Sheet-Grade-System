Module src.routes.quiz_route
============================

Functions
---------

`add_quiz() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Add a new quiz to the database.
    
    This route accepts the quiz data (title, description, questions, and teacher ID) and creates a new quiz record.
    
    Returns:
        jsonify: The created quiz data with a 201 CREATED status, or an error message with a 400 BAD REQUEST status.

`delete_quiz(quiz_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Delete a specific quiz by its ID.
    
    This route deletes a quiz based on the provided `quiz_id`. If the quiz is not found, a 400 error is returned.
    
    Args:
        quiz_id (str): The ID of the quiz to delete.
    
    Returns:
        jsonify: The deletion result with a 200 OK status, or an error message with a 400 BAD REQUEST status.

`export_pdf(quiz_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Export a quiz to a PDF file.
    
    This route generates a PDF of the specified quiz and its associated teacher. The PDF is returned as an attachment.
    
    Args:
        quiz_id (str): The ID of the quiz to export to PDF.
    
    Returns:
        send_file: The generated PDF file as a downloadable attachment, or an error message with a 400 status if
        not found.

`get_by_teacher_id(teacher_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieve all quizzes created by a specific teacher.
    
    This route returns a list of quizzes associated with the given teacher ID.
    
    Args:
        teacher_id (str): The ID of the teacher whose quizzes are to be retrieved.
    
    Returns:
        jsonify: A list of quizzes with a 200 OK status, or an error message with a 400 BAD REQUEST status.

`get_quiz(quiz_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieve a specific quiz by its ID.
    
    This route retrieves a quiz based on the provided `quiz_id`. If no quiz is found, it returns a 404 error.
    
    Args:
        quiz_id (str): The ID of the quiz to retrieve.
    
    Returns:
        jsonify: The quiz data with a 200 OK status, or an error message with a 404 status if not found.

`get_quizzes() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieve the list of all quizzes.
    
    This route returns a list of quizzes stored in the database.
    
    Returns:
        jsonify: A list of quizzes with a 200 OK status.

`grade() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Grade a quiz based on an image submission.
    
    This route accepts an image containing the completed quiz, processes it, and returns the grading results.
    
    Returns:
        jsonify: The grading results with a 200 OK status, or an error message with a 400 BAD REQUEST status.

`update_quiz(quiz_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Update an existing quiz.
    
    This route allows updating quiz details based on the `quiz_id`. The provided data will overwrite the existing quiz.
    
    Args:
        quiz_id (str): The ID of the quiz to update.
    
    Returns:
        jsonify: The updated quiz data with a 200 OK status, or an error message with a 400 BAD REQUEST status.