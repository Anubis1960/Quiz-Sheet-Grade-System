import logging
from typing import Dict

from src.database import db
from src.models.student import Student

COLLECTION_NAME = 'students'


#
#	Retrieve all students
#
def get_students_data() -> list[Student]:
    logging.info("\tService Layer ==>	Retrieve students loading...")

    # Fetch students data
    students_data = db.collection(COLLECTION_NAME).stream()

    # Process data
    students_list = [student.to_dict() for student in students_data]

    print(students_list)

    logging.info("\tService Layer ==>	Successfully retrieved students list.")
    return students_list


#
#   Retrieve student by id
#
def get_student_by_id(student_id: str) -> dict:
    logging.info("\tService Layer ==>	Retrieve student by id loading...")
    # Fetch the document from the Firestore Database
    student_data = db.collection(COLLECTION_NAME).document(student_id).get()

    # Verify if the student exists in the collection
    if not student_data.exists:
        logging.warning(f"\tService Layer ==>	No data found for student with id: {student_id}")
        return {}

    logging.info(f"\tService Layer ==>	Successfully retrieved student with id: {student_id}")

    return student_data


####################################
#
#   CRUD Operations
#
####################################

#
#   Add
#
def create_student(student: Student) -> Student | None:
    try:
        logging.info("\tService Layer ==>	Create student loading...")
        # Convert student to dictionary

        # Add student into database
        db.collection(COLLECTION_NAME).add(student.to_dict())
        logging.info("\tService Layer ==>	Student added successfully.")

        return student

    except KeyError as e:
        return None


#
#	Update
#


#
#   Delete 
#  
def delete_student_by_id(student_id: str) -> dict[str, str]:
    try:
        logging.info("\tService Layer ==>	Delete student loading...")
        # Fetch student data based on id
        get_student_by_id(student_id)

        # Delete the reference of the student
        student_ref = db.collection(COLLECTION_NAME).document(student_id)

        logging.info("\tService Layer ==>	Student deleted successfully.")
        student_ref.delete()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}
