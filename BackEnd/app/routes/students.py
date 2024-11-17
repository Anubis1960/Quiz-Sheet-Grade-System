from flask import Blueprint, request, jsonify
from services.student_service import create_student,get_student_by_id
from entities.Student import Student

student_blueprint = Blueprint('student',__name__)

@student_blueprint.route("/",methods = ['POST'])
def add_student():
    try:
        data = request.get_json()
        print("Incoming data: ",data)

        unique_id = data['unique_id']
        email = data['email']

        student = Student(unique_id = unique_id,email = email)
        result = create_student(student)
        print("Result from 'create_student():",result)
        return jsonify(result), 200
    except Exception as e:
        return {"message": str(e)}, 500
    
@student_blueprint.route("/<student_id>", methods = ['GET'])
def get_student(student_id):
    try:
        print("Inside 'get_student()...")
        result = get_student_by_id(student_id)
        print("Student received from the service: ", result.to_dict())

        # Verify if result is a dictionary and contains an 'error' key
        if isinstance(result,dict) and "error" in result:
            return jsonify(result), 404
        return jsonify(result.to_dict()), 200
    except Exception as e:
        return {"message": str(e)}
