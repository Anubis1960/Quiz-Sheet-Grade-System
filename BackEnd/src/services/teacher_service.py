import logging
from src.database import db
from src.entities.Teacher import Teacher

COLLECTION_NAME = 'teachers'

####################################
#
#   CRUD Operations
#
####################################

#
#  Retrieve teachers
#
def get_teachers_data():
	logging.info("\tService Layer ==>	Retrieve teachers loading...")
	
	# Fetch teachers data from Firestore
	teachers_data = db.collection(COLLECTION_NAME).stream()

	# Process data
	teachers_list = []
	for teacher in teachers_data:
		teacher_dict = teacher.to_dict()  
		teacher_dict['id'] = teacher.id 
		teachers_list.append(teacher_dict)

	# Check if data exists
	if not teachers_list:
		logging.warning("\tService Layer ==>	No teachers in database.")
		return None
	
	logging.info("\tService Layer ==>	Successfully retrieved teachers data.")
	return teachers_list
		

#
#   Retrieve teacher by id
#
def get_teacher_by_id(teacher_id):
	try:
		print("Inside get_teacher_by_id...")
		# Fetch the document from Firestore
		doc = db.collection(COLLECTION_NAME).document(teacher_id).get()

		if doc.exists:
			print("doc exists...")
			# Convert Firestore data into a Teacher object
			teacher = Teacher.from_dict(doc.to_dict())
			print("Retreived Teacher: ",teacher.to_dict())
			return teacher
	except Exception as e:
		return {"error:": str(e)}
	
#
#   Add teacher
#
def create_teacher(teacher: Teacher):
	# Convert teacher to dictionary
	teacher_data = teacher.to_dict()
	print("Teacher data:",teacher_data)
	try: 
		# Add teacher data to firestore
		_,teacher_ref = db.collection(COLLECTION_NAME).add(teacher_data)
		return {"message": f"Teacher {teacher.name} added with ID: {teacher_ref.id}"}
	except Exception as e:
		return {"error:": str(e)}

#
#   Delete teacher by id
#
def delete_teacher_by_id(teacher_id):
	try:
		print("Inside delete_teacher in service...")
		teacher_to_be_deleted = get_teacher_by_id(teacher_id)

		# if "error" in teacher_to_be_deleted:
		#     return teacher_to_be_deleted
		print("Teacher to be deleted is: ", teacher_to_be_deleted.to_dict())

		# Delete the reference of the teacher
		teacher_ref = db.collection(COLLECTION_NAME).document(teacher_id)
		teacher_ref.delete()

		return {"message": f"Teacher with ID: {teacher_id} deleted successfully"}
	except Exception as e:
		return {"error:": str(e)}
