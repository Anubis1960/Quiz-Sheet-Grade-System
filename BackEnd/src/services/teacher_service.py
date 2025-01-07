from src.database import db
from src.models.teacher import Teacher

COLLECTION = 'teachers'


#
#  Retrieve teachers
#
def get_teachers_data() -> list[dict]:
    teachers_data = db.collection(COLLECTION).stream()
    teachers_list = [teacher.to_dict() for teacher in teachers_data]
    return teachers_list


#
#   Retrieve teacher by id
#
def get_teacher_by_id(teacher_id: str) -> dict:
    teacher_snapshot = db.collection(COLLECTION).document(teacher_id).get()
    if teacher_snapshot.exists:
        return teacher_snapshot.to_dict()
    return {}


#
#   Add teacher
#
def create_teacher(teacher: Teacher) -> dict:
    try:
        db.collection(COLLECTION).add(teacher.to_dict())

        if get_teacher_by_email(teacher.email):
            return {"error": f"An account with email {teacher.email} already exists."}

        return teacher.to_dict()

    except KeyError as e:
        return {"error": f"Key Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


#
#   Update teacher by id
#
def update_teacher_by_id(teacher_id: str, teacher: Teacher) -> dict:
    try:
        teacher_ref = db.collection(COLLECTION).document(teacher_id)

        teacher_snapshot = teacher_ref.get()
        if not teacher_snapshot.exists:
            return {"error": f"No data found for id: {teacher_id}"}

        if teacher_ref.get().to_dict()['email'] != teacher.email:
            if get_teacher_by_email(teacher.email):
                return {"error": f"An account with email {teacher.email} already exists."}

        teacher_ref.update(teacher.to_dict())
        return teacher.to_dict()

    except KeyError as e:
        return {"error": f"Key missing: {str(e)}"}

    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


#
#   Delete teacher by id
#
def delete_teacher_by_id(teacher_id: str) -> dict:
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


def get_teacher_by_email(email: str) -> list[dict]:
    teacher = db.collection(COLLECTION).where('email', '==', email).stream()
    return [t.to_dict() for t in teacher]
