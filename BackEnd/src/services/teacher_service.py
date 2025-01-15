from src.database import db
from src.models.teacher import Teacher
from src.models.teacherDTO import TeacherDTO
import re

COLLECTION = 'teachers'
REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def get_teachers_data() -> list[dict]:
    """
    Retrieve all teacher data from the database.

    Returns:
        list[dict]: A list of dictionaries containing teacher data.
    """
    teachers_data = db.collection(COLLECTION).stream()
    teachers_list = [teacher.to_dict() for teacher in teachers_data]
    return teachers_list


def get_teacher_by_id(teacher_id: str) -> dict:
    """
    Retrieve a teacher's data by their unique ID.

    Args:
        teacher_id (str): The ID of the teacher to retrieve.

    Returns:
        dict: A dictionary containing the teacher's data, or an empty dictionary if not found.
    """
    teacher_snapshot = db.collection(COLLECTION).document(teacher_id).get()
    if teacher_snapshot.exists:
        return teacher_snapshot.to_dict()
    return {}


def create_teacher(teacher: Teacher) -> dict:
    """
    Add a new teacher to the database.

    Args:
        teacher (Teacher): The Teacher object containing the data to add.

    Returns:
        dict: A dictionary containing the added teacher's data or an error message.
    """
    try:
        if not re.match(REGEX, teacher.email):
            return {"error": "Invalid email format."}
        if get_teacher_by_email(teacher.email):
            return {"error": f"An account with email {teacher.email} already exists."}

        _, teacher_ref = db.collection(COLLECTION).add(teacher.to_dict())

        teacherDTO = TeacherDTO(teacher_ref.id, teacher.name, teacher.email)

        return teacherDTO.to_dict()

    except KeyError as e:
        return {"error": f"Key Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def update_teacher_by_id(teacher_id: str, teacher: Teacher) -> dict:
    """
    Update a teacher's data by their unique ID.

    Args:
        teacher_id (str): The ID of the teacher to update.
        teacher (Teacher): The Teacher object containing the updated data.

    Returns:
        dict: A dictionary containing the updated teacher's data or an error message.
    """
    try:
        teacher_ref = db.collection(COLLECTION).document(teacher_id)

        teacher_snapshot = teacher_ref.get()
        if not teacher_snapshot.exists:
            return {"error": f"No data found for id: {teacher_id}"}

        if not re.match(REGEX, teacher.email):
            return {"error": "Invalid email format."}

        if teacher_ref.get().to_dict()['email'] != teacher.email:
            if get_teacher_by_email(teacher.email):
                return {"error": f"An account with email {teacher.email} already exists."}

        teacher_ref.update(teacher.to_dict())
        return teacher.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


def delete_teacher_by_id(teacher_id: str) -> dict:
    """
    Delete a teacher's data by their unique ID.

    Args:
        teacher_id (str): The ID of the teacher to delete.

    Returns:
        dict: A dictionary containing the deleted teacher's data or an error message.
    """
    try:
        teacher_ref = db.collection(COLLECTION).document(teacher_id)

        teacher_snapshot = teacher_ref.get()
        if not teacher_snapshot.exists:
            return {"error": f"No data found for id: {teacher_id}"}

        teacher_ref.delete()
        return teacher_snapshot.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


def get_teacher_by_email(email: str) -> dict:
    """
    Retrieve a teacher's data by their email address.

    Args:
        email (str): The email address of the teacher to retrieve.

    Returns:
        dict: A dictionary containing the teacher's data or an empty dictionary if not found.
    """
    teachers = list(db.collection(COLLECTION).where('email', '==', email).stream())

    if len(teachers) == 0:
        return {}

    teacher_doc = teachers[0]
    teacher_data = teacher_doc.to_dict()

    teacherDTO = TeacherDTO(teacher_doc.id, teacher_data['name'], teacher_data['email'])

    return teacherDTO.to_dict()


def get_teacher_by_email_and_password(email: str, password: str) -> dict:
    """
    Retrieve a teacher's data by their email address and password.

    Args:
        email (str): The email address of the teacher.
        password (str): The password of the teacher.

    Returns:
        dict: A dictionary containing the teacher's data or an empty dictionary if not found.
    """
    teachers = list(db.collection(COLLECTION)
                    .where('email', '==', email)
                    .where('password', '==', password)
                    .stream())

    if len(teachers) == 0:
        return {}

    teacher_doc = teachers[0]
    teacher_data = teacher_doc.to_dict()

    teacherDTO = TeacherDTO(teacher_doc.id, teacher_data['name'], teacher_data['email'])

    return teacherDTO.to_dict()
