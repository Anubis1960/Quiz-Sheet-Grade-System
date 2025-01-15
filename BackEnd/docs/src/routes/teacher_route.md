Module src.routes.teacher_route
===============================

Functions
---------

`add_teacher() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Adds a new teacher to the database.
    
    This endpoint accepts a POST request with the following JSON body:
    - `name`: The name of the teacher.
    - `email`: The email of the teacher.
    - `password`: The password for the teacher (will be encrypted before storing).
    
    Returns:
        jsonify: The newly created teacher data in JSON format.
        HTTPStatus: 201 CREATED if the teacher is successfully created, 400 BAD REQUEST if validation fails.

`delete_teacher(teacher_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Deletes a teacher from the database based on the provided teacher ID.
    
    Args:
        teacher_id (str): The ID of the teacher to delete.
    
    Returns:
        jsonify: The deleted teacher's data in JSON format.
        HTTPStatus: 200 OK if successfully deleted, 404 NOT FOUND if no teacher exists with the provided ID.

`get_by_email(email: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieves a teacher's data based on the provided email.
    
    Args:
        email (str): The email of the teacher to retrieve.
    
    Returns:
        jsonify: The teacher's data in JSON format if found.
        HTTPStatus: 200 OK if the teacher is found, 404 NOT FOUND if no teacher exists with the provided email.

`get_teacher(teacher_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieves a specific teacher's data based on the provided teacher ID.
    
    Args:
        teacher_id (str): The ID of the teacher to retrieve.
    
    Returns:
        jsonify: The teacher's data in JSON format if found.
        HTTPStatus: 200 OK if successful, 404 NOT FOUND if no data found for the provided ID.

`get_teachers() ‑> <function jsonify at 0x000002A05DE14E00>`
:   Retrieves a list of all teachers from the database.
    
    This endpoint accepts a GET request and returns a list of teachers in JSON format.
    
    Returns:
        jsonify: A list of teachers in JSON format.
        HTTPStatus: 200 OK if successful.

`update_teacher(teacher_id: str) ‑> <function jsonify at 0x000002A05DE14E00>`
:   Updates the data of an existing teacher in the database.
    
    Args:
        teacher_id (str): The ID of the teacher to update.
    
    This endpoint accepts a PUT request with the following JSON body:
    - `name`: The updated name of the teacher.
    - `email`: The updated email of the teacher.
    - `password`: The updated password for the teacher (will be encrypted before storing).
    
    Returns:
        jsonify: The updated teacher data in JSON format.
        HTTPStatus: 200 OK if the teacher is successfully updated, 400 BAD REQUEST if validation fails.