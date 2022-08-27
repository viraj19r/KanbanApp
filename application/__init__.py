from flask import Flask
from application.config import LocalDevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from application.database import db

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login' # pass login function name here
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
app = None

def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    app.config.from_object(LocalDevelopmentConfig)
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    app.app_context().push()
    return app

app = create_app()


@app.before_first_request
def init_app():
    logout_user()

from application.controllers import *
from application.api import *

