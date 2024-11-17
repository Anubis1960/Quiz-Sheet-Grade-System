from flask import Blueprint,request,jsonify
from services.teacher_service import create_teacher, get_teacher_by_id, delete_teacher_by_id
from entities.Teacher import Teacher

teacher_blueprint = Blueprint('teacher',__name__)

# Route to add a teacher into the Firestore Database
@teacher_blueprint.route('/',methods = ['POST'])
def add_teacher():
    try:
        data = request.get_json()
        print("Incoming data",data)

        name = data['name']
        email = data['email']
        password = data['password']

        teacher = Teacher(name = name,email = email,password = password)
        result = create_teacher(teacher)
        print("Result from create_teacher():" , result)

        return jsonify(result),200
    except Exception as e:
        return {"error:":str(e)}, 500

# Route to get a teacher from the Firestore Database
@teacher_blueprint.route('/<teacher_id>',methods = {'GET'})
def get_teacher(teacher_id):
    try:
        print("Inside get_teacher...")
        result = get_teacher_by_id(teacher_id)
        print("Teacher retrieved from the service:", result.to_dict())

        # Verify if result is a dictionary and contains an 'error' key
        if isinstance(result,dict) and "error" in result:
            return jsonify(result), 404

        return jsonify(result.to_dict()),200

    except Exception as e:
        return {"error:":str(e)}, 500

# Route to delete a teacher from Firestore Database
@teacher_blueprint.route('/<teacher_id>',methods = {'DELETE'})
def delete_teacher(teacher_id):
    try:
        print("Inside delete_teacher...")
        teacher_to_be_deleted = delete_teacher_by_id(teacher_id)
        print("Teacher to be deleted: ", teacher_to_be_deleted)
        if isinstance(teacher_to_be_deleted,dict) and "error" in teacher_to_be_deleted:
            return jsonify(teacher_to_be_deleted), 404
        
        return jsonify(teacher_to_be_deleted), 200
    except Exception as e:
        return {"error:": str(e)}, 500
