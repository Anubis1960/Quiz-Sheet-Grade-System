Module src.services.student_service
===================================

Variables
---------

`COLLECTION`
:   Service functions for managing student data in the Firestore database.

Functions
---------

`create_student(student: src.models.student.Student) ‑> dict`
:   Add a new student to the database.
    
    Args:
        student (Student): The Student object containing the data to add.
    
    Returns:
        dict: A dictionary containing the added student's data or an error message.

`delete_student_by_id(student_id: str) ‑> dict`
:   Delete a student's data by their unique ID.
    
    Args:
        student_id (str): The ID of the student to delete.
    
    Returns:
        dict: A dictionary containing the deleted student's data or an error message.

`get_student_by_id(student_id: str) ‑> dict`
:   Retrieve a student's data by their unique ID.
    
    Args:
        student_id (str): The ID of the student to retrieve.
    
    Returns:
        dict: A dictionary containing the student's data or an empty dictionary if not found.

`get_student_by_unique_id(unique_id: str) ‑> list[dict]`
:   Retrieve student data by a unique identifier.
    
    Args:
        unique_id (str): The unique identifier for the student.
    
    Returns:
        list[dict]: A list of dictionaries containing the students' data matching the unique ID.

`get_students_data() ‑> list[src.models.student.Student]`
:   Retrieve all student data from the database.
    
    Returns:
        list[Student]: A list of Student objects containing all students' data.

`update_student_data(student_id: str, student: src.models.student.Student) ‑> dict`
:   Update a student's data by their unique ID.
    
    Args:
        student_id (str): The ID of the student to update.
        student (Student): The Student object containing the updated data.
    
    Returns:
        dict: A dictionary containing the updated student's data or an error message.