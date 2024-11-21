import logging
from src.database import db
from src.models.teacher import Teacher
from src.exceptions.NoDataFoundError import NoDataFoundError

COLLECTION_NAME = 'teachers'


#
#  Retrieve teachers
#
def get_teachers_data() -> list[dict]:
    logging.info("\tService Layer ==>	Retrieve teachers loading...")

    # Fetch teachers data from Firestore
    teachers_data = db.collection(COLLECTION_NAME).stream()

    # Process data
    teachers_list = [teacher.to_dict() for teacher in teachers_data]

    logging.info("\tService Layer ==>	Successfully retrieved teachers data.")
    return teachers_list


#
#   Retrieve teacher by id
#
def get_teacher_by_id(teacher_id: str) -> dict:
    logging.info("\tService Layer ==>	Retrieve teacher by id loading...")

    # Fetch the document from Firestore
    teacher_snapshot = db.collection(COLLECTION_NAME).document(teacher_id).get()

    if not teacher_snapshot.exists:
        logging.warning(f"\tService Layer ==>	No data found for teacher with id: {teacher_id}")
        return None

    logging.info(f"\tService Layer ==>	Successfully retrieved teacher with id: {teacher_id}")
    return teacher_snapshot.to_dict()


####################################
#
#   CRUD Operations
#
####################################

#
#   Add teacher
#
def create_teacher(teacher: Teacher) -> None:
    logging.info("\tRoutes Layer ==>	Adding new teacher loading...")

    # Converting teacher into dict
    teacher_dict = teacher.to_dict()

    #
    #	Validations
    #

    try:
        # Retrieve existing teachers
        teachers_list = get_teachers_data()

        # Check for duplicate email if the list is not empty
        for teacher_data in teachers_list:
            if teacher_data['email'] == teacher_dict['email']:
                logging.warning(f"\tEmail: {teacher_dict['email']} already existing.")
                raise ValueError(f"Teacher email: {teacher_dict['email']} already exists.")

    except NoDataFoundError:
        # Handle case where no teachers exist
        logging.info("\tService Layer ==> No existing teachers. Proceeding with the addition.")

    # Add teacher data to firestore
    db.collection(COLLECTION_NAME).add(teacher_dict)
    logging.info("\tService Layer ==>	Successfully added teacher.")


#
#   Delete teacher by id
#
def delete_teacher_by_id(teacher_id: str) -> None:
    # Fetch teacher by id
    teacher_dict = get_teacher_by_id(teacher_id)

    # Verify if teacher_dict exists
    if teacher_dict is None:
        logging.warning("\tService Layer ==> Teacher not found.")
        raise LookupError(f"Teacher with ID '{teacher_id}' not found.")

    # Delete the reference of the teacher
    db.collection(COLLECTION_NAME).document(teacher_id).delete()
    logging.info("\tService Layer ==>	Teacher deleted successfully.")
