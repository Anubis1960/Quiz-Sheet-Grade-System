from database import db
from entities.Teacher import Teacher

def create_teacher(teacher: Teacher):
    # Convert teacher to dictionary
    teacher_data = teacher.to_dict()
    print("Teacher data:",teacher_data)
    try: 
        # Add teacher data to firestore
        _,teacher_ref = db.collection('teachers').add(teacher_data)
        return {"message": f"Teacher {teacher.name} added with ID: {teacher_ref.id}"}
    except Exception as e:
        return {"error:": str(e)}

def get_teacher_by_id(teacher_id):
    try:
        print("Inside get_teacher_by_id...")
        # Fetch the document from Firestore
        doc = db.collection('teachers').document(teacher_id).get()

        if doc.exists:
            print("doc exists...")
            # Convert Firestore data into a Teacher object
            teacher = Teacher.from_dict(doc.to_dict())
            print("Retreived Teacher: ",teacher.to_dict())
            return teacher
    except Exception as e:
        return {"error:": str(e)}

def delete_teacher_by_id(teacher_id):
    try:
        print("Inside delete_teacher in service...")
        teacher_to_be_deleted = get_teacher_by_id(teacher_id)

        # if "error" in teacher_to_be_deleted:
        #     return teacher_to_be_deleted
        print("Teacher to be deleted is: ", teacher_to_be_deleted.to_dict())

        # Delete the reference of the teacher
        teacher_ref = db.collection('teachers').document(teacher_id)
        teacher_ref.delete()

        return {"message": f"Teacher with ID: {teacher_id} deleted successfully"}
    except Exception as e:
        return {"error:": str(e)}
