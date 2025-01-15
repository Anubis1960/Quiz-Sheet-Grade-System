Module src.routes.student_route
===============================

Functions
---------

`add_student() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Adds a new student to the database.
    
    This endpoint accepts a POST request with the following JSON body:
    - `unique_id`: The unique identifier of the student.
    - `email`: The email of the student (must be valid format).
    
    Returns:
        jsonify: The newly created student's data in JSON format.
        HTTPStatus: 201 CREATED if the student is successfully created, 400 BAD REQUEST if validation fails.

`delete_student(student_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Deletes a student from the database based on the provided student ID.
    
    Args:
        student_id (str): The ID of the student to delete.
    
    Returns:
        jsonify: The deleted student's data in JSON format.
        HTTPStatus: 200 OK if successfully deleted, 404 NOT FOUND if no student exists with the provided ID.

`get_student(student_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieves a specific student's data based on the provided student ID.
    
    Args:
        student_id (str): The ID of the student to retrieve.
    
    Returns:
        jsonify: The student's data in JSON format if found.
        HTTPStatus: 200 OK if successful, 404 NOT FOUND if no data found for the provided ID.

`get_students() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieves a list of all students from the database.
    
    This endpoint accepts a GET request and returns a list of students in JSON format.
    
    Returns:
        jsonify: A list of students in JSON format.
        HTTPStatus: 200 OK if successful.

`update_student(student_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Updates the data of an existing student in the database.
    
    Args:
        student_id (str): The ID of the student to update.
    
    This endpoint accepts a PUT request with the following JSON body:
    - `unique_id`: The updated unique identifier of the student.
    - `email`: The updated email of the student (must be valid format).
    
    Returns:
        jsonify: The updated student's data in JSON format.
        HTTPStatus: 200 OK if successful, 400 BAD REQUEST if validation fails.