import logging
from flask import Flask
from src.routes.teacher_route import teacher_blueprint
from src.routes.student_route import student_blueprint
from src.routes.quiz_route import quiz_blueprint

####################
#
#   Add the path to the project
#
####################
import sys

sys.path.append("src")

app = Flask(__name__)

####################
#
#   Logging config
#
####################
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

####################
#
#   Blueprints Init
#
####################
app.register_blueprint(teacher_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(quiz_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
