from database import db
from entities.Student import Student
from google.cloud.firestore_v1.base_query import FieldFilter
def create_student(student: Student):
    # Convert student to dictionary
    student_data = student.to_dict()
    print("Student to be added in Firestore: ",student_data)
    try:
        print("Inside 'create_student' funtion...")
        # students_ref = db.collection('students')

        # # Check if there is another student with the same unique_id
        # existing_student_unique_id = students_ref.where(filter=FieldFilter("unique_id","==",student_data["unique_id"]))
        # if existing_student_unique_id:
        #     return {"error": f"Student with unique_id: {student.unique_id} already exists in collection 'students'."}
        
        # # Check if there is another student with the same email
        # existing_student_email = student.ref.where(filter=FieldFilter("email","==",student.email))
        # if existing_student_email:
        #     return {"error": f"Student with email: {student.email} already exists in collection 'students'."}
        
        # Add the student to the Firestore Database in 'students' collection
        _,student_ref = db.collection('students').add(student_data)
        return {"message": f"Student with unique_id {student.unique_id} and with {student_ref.id} code in Firestore created successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_student_by_id(student_id):
    try:
        # Fetch the document from the Firestore Database
        doc = db.collection('students').document(student_id).get()
        # Verify if the student exists in the collection
        if doc.exists:
            print("Student exists..")
            # Convert the Firestore data into a Student object
            student = Student.from_dict(doc.to_dict())
            print("Student received: ", student.to_dict())
            return student
    except Exception as e:
        return {"error": str(e)}
    
def delete_student_by_id(student_id):
    try:
        print("Inside delete_student_by_id()...")
        student_to_be_deleted = get_student_by_id(student_id)
        print("Student to be deleted is: ", student_to_be_deleted.to_dict())

        # Delete the reference of the student
        student_ref = db.collection('students').document(student_id)
        student_ref.delete()

        return {"message":f"Student with id: {student_id} deleted successfully"}
    except Exception as e:
        return {"message":str(e)}