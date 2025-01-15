import logging
import os
####################
#
#   Add the path to the project
#
####################
import sys

from flask import Flask
from flask_cors import CORS

from src.models.oauthmanager import OAuthManager
from src.routes.auth_route import auth_blueprint
from src.routes.quiz_route import quiz_blueprint
from src.routes.student_route import student_blueprint
from src.routes.teacher_route import teacher_blueprint
from src.routes.token_route import token_blueprint

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

app.register_blueprint(token_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
