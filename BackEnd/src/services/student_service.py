from google.cloud.firestore_v1 import FieldFilter

from src.database import db
from src.models.student import Student

COLLECTION = 'students'

"""
Service functions for managing student data in the Firestore database.
"""


def get_students_data() -> list[Student]:
    """
    Retrieve all student data from the database.

    Returns:
        list[Student]: A list of Student objects containing all students' data.
    """
    students = db.collection(COLLECTION).stream()
    students_list = [student.to_dict() for student in students]
    return students_list


def get_student_by_id(student_id: str) -> dict:
    """
    Retrieve a student's data by their unique ID.

    Args:
        student_id (str): The ID of the student to retrieve.

    Returns:
        dict: A dictionary containing the student's data or an empty dictionary if not found.
    """
    student_data = db.collection(COLLECTION).document(student_id).get()
    if student_data.exists:
        return student_data.to_dict()
    return {}


def get_student_by_unique_id(unique_id: str) -> list[dict]:
    """
    Retrieve student data by a unique identifier.

    Args:
        unique_id (str): The unique identifier for the student.

    Returns:
        list[dict]: A list of dictionaries containing the students' data matching the unique ID.
    """
    students = db.collection(COLLECTION).where(filter=FieldFilter("unique_id", "==", unique_id)).stream()
    student_list = [student.to_dict() for student in students]
    return student_list


def create_student(student: Student) -> dict:
    """
    Add a new student to the database.

    Args:
        student (Student): The Student object containing the data to add.

    Returns:
        dict: A dictionary containing the added student's data or an error message.
    """
    try:
        db.collection(COLLECTION).add(student.to_dict())
        return student.to_dict()

    except KeyError as e:
        return {"error": f"Key Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def update_student_data(student_id: str, student: Student) -> dict:
    """
    Update a student's data by their unique ID.

    Args:
        student_id (str): The ID of the student to update.
        student (Student): The Student object containing the updated data.

    Returns:
        dict: A dictionary containing the updated student's data or an error message.
    """
    try:
        student_ref = db.collection(COLLECTION).document(student_id)

        student_snapshot = student_ref.get()
        if not student_snapshot.exists:
            return {"error": f"No data found for id: {student_id}"}

        student_ref.update(student.to_dict())
        return student.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def delete_student_by_id(student_id: str) -> dict:
    """
    Delete a student's data by their unique ID.

    Args:
        student_id (str): The ID of the student to delete.

    Returns:
        dict: A dictionary containing the deleted student's data or an error message.
    """
    try:
        student_ref = db.collection(COLLECTION).document(student_id)

        student_snapshot = student_ref.get()
        if not student_snapshot.exists:
            return {"error": f"No data found for id: {student_id}"}

        student = student_ref.get().to_dict()

        student_ref.delete()

        return student

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}