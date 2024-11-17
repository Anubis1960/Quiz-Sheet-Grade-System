from flask import Flask
from routes.teachers import teacher_blueprint
from routes.students import student_blueprint

app = Flask(__name__)

app.register_blueprint(teacher_blueprint,url_prefix = '/teachers')
app.register_blueprint(student_blueprint, url_prefix = '/students')
if __name__ == '__main__':
    app.run(debug = True)