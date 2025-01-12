import os
import logging
from flask import Flask
from src.routes.teacher_route import teacher_blueprint
from src.routes.student_route import student_blueprint
from src.routes.quiz_route import quiz_blueprint
from src.routes.auth_route import auth_blueprint
from src.models.oauthmanager import OAuthManager
from flask_cors import CORS

####################
#
#   Add the path to the project
#
####################
import sys

sys.path.append("src")

app = Flask(__name__)

app.secret_key = os.urandom(24)

CORS(app)

# OAuth Manager Setup
oauth_manager = OAuthManager(app)
app.oauth_manager = oauth_manager

####################
#
#   Logging config
#
####################
logging.basicConfig(
	level=logging.DEBUG,
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
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
	app.run(debug=True)
