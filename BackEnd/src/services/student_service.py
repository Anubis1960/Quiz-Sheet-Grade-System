import logging
from src.database import db
from src.entities.Student import Student

COLLECTION_NAME = 'students'

#
#	Retrieve all students
#
def get_students_data() -> list[Student]:
	logging.info("\tService Layer ==>	Retrieve students loading...")

	# Fetch students data 
	students_data = db.collection(COLLECTION_NAME).stream()

	# Process data
	students_list = []
	for student in students_data:
		student_dict = student.to_dict()
		student_dict['id'] = student.id
		students_list.append(student_dict)

	# Check if data exists
	if not students_list:
		logging.warning("\tService Layer ==>	No students in database.")
		return None
	
	logging.info("\tService Layer ==>	Successfully retrieved students list.")
	return students_list


#
#   Retrieve student by id
#
def get_student_data_by_id(student_id: str) -> Student:
	logging.info("\tService Layer ==>	Retrieve student by id loading...")
	# Fetch the document from the Firestore Database
	student_data = db.collection(COLLECTION_NAME).document(student_id).get()

	# Verify if the student exists in the collection
	if student_data is None:
		logging.warning(f"\tService Layer ==>	No data found for student with id: {student_id}")
		return None
	
	# Convert the Firestore data into a Student object
	student = Student.from_dict(student_data.to_dict())

	logging.info(f"\tService Layer ==>	Successfully retrieved student with id: {student_id}")
	
	return student

	
####################################
#
#   CRUD Operations
#
####################################

#
#   Add
#
def create_student(student: Student) -> None:
	try:
		logging.info("\tService Layer ==>	Create student loading...")
		# Convert student to dictionary
		student_data = student.to_dict()

		# Add student into database
		db.collection(COLLECTION_NAME).add(student_data)
		logging.info("\tService Layer ==>	Student added successfully.")
		
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

#
#	Update
#
# TODO:

#
#   Delete 
#  
def delete_student_by_id(student_id: str) -> None:
	try:
		logging.info("\tService Layer ==>	Delete student loading...")
		# Fetch student data based on id
		get_student_data_by_id(student_id)

		# Delete the reference of the student
		student_ref = db.collection(COLLECTION_NAME).document(student_id)

		logging.info("\tService Layer ==>	Student deleted successfully.")
		student_ref.delete()

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}