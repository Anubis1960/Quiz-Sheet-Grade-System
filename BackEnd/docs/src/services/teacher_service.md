Module src.services.teacher_service
===================================

Functions
---------

`create_teacher(teacher: src.models.teacher.Teacher) ‑> dict`
:   Add a new teacher to the database.
    
    Args:
        teacher (Teacher): The Teacher object containing the data to add.
    
    Returns:
        dict: A dictionary containing the added teacher's data or an error message.

`delete_teacher_by_id(teacher_id: str) ‑> dict`
:   Delete a teacher's data by their unique ID.
    
    Args:
        teacher_id (str): The ID of the teacher to delete.
    
    Returns:
        dict: A dictionary containing the deleted teacher's data or an error message.

`get_teacher_by_email(email: str) ‑> dict`
:   Retrieve a teacher's data by their email address.
    
    Args:
        email (str): The email address of the teacher to retrieve.
    
    Returns:
        dict: A dictionary containing the teacher's data or an empty dictionary if not found.

`get_teacher_by_email_and_password(email: str, password: str) ‑> dict`
:   Retrieve a teacher's data by their email address and password.
    
    Args:
        email (str): The email address of the teacher.
        password (str): The password of the teacher.
    
    Returns:
        dict: A dictionary containing the teacher's data or an empty dictionary if not found.

`get_teacher_by_id(teacher_id: str) ‑> dict`
:   Retrieve a teacher's data by their unique ID.
    
    Args:
        teacher_id (str): The ID of the teacher to retrieve.
    
    Returns:
        dict: A dictionary containing the teacher's data, or an empty dictionary if not found.

`get_teachers_data() ‑> list[dict]`
:   Retrieve all teacher data from the database.
    
    Returns:
        list[dict]: A list of dictionaries containing teacher data.

`update_teacher_by_id(teacher_id: str, teacher: src.models.teacher.Teacher) ‑> dict`
:   Update a teacher's data by their unique ID.
    
    Args:
        teacher_id (str): The ID of the teacher to update.
        teacher (Teacher): The Teacher object containing the updated data.
    
    Returns:
        dict: A dictionary containing the updated teacher's data or an error message.