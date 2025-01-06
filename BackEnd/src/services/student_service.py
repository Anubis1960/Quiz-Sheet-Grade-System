from google.cloud.firestore_v1 import FieldFilter

from src.database import db
from src.models.student import Student

COLLECTION = 'students'


#
#	Retrieve all students
#
def get_students_data() -> list[Student]:
    students = db.collection(COLLECTION).stream()
    students_list = [student.to_dict() for student in students]
    return students_list


#
#   Retrieve student by id
#
def get_student_by_id(student_id: str) -> dict:
    student_data = db.collection(COLLECTION).document(student_id).get()
    if student_data.exists:
        return student_data.to_dict()
    return {}


def get_student_by_unique_id(unique_id: str) -> list[dict]:
    students = db.collection(COLLECTION).where(filter=FieldFilter("unique_id", "==", unique_id)).stream()
    student_list = [student.to_dict() for student in students]
    return student_list


#
#   Add
#
def create_student(student: Student) -> dict:
    try:
        db.collection(COLLECTION).add(student.to_dict())
        return student.to_dict()

    except KeyError as e:
        return {"error": f"Key Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


#
#	Update
#
def update_student_data(student_id: str, student: Student) -> dict:
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


#
#   Delete 
#  
def delete_student_by_id(student_id: str) -> dict:
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
