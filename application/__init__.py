from flask import Flask
from application.config import LocalDevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from application.database import db

login_manager = LoginManager() # create instance of login manager class from flask-login
login_manager.session_protection = 'strong'
login_manager.login_view = 'login' # pass login function name here
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
app = None

def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')# set the location of templates and static folder manually
    app.config.from_object(LocalDevelopmentConfig) # configure the basic config setting fron config.py
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    app.app_context().push() # push app context beyond the context of this app so that database can access it
    return app

app = create_app()

# logout any existing user before first app request
@app.before_first_request
def init_app():
    logout_user()

#load all the controllers here
from application.controllers import *
from application.api import *

