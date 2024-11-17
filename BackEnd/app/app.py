from flask import Flask
from routes.teachers import teacher_blueprint
from routes.students import student_blueprint
from routes.quizzes import quiz_blueprint

app = Flask(__name__)

app.register_blueprint(teacher_blueprint,url_prefix = '/teachers')
app.register_blueprint(student_blueprint, url_prefix = '/students')
app.register_blueprint(quiz_blueprint, url_prefix = '/quizzes')

if __name__ == '__main__':
    app.run(debug = True)