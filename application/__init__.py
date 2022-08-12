from application.controllers import *
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_bcrypt import Bcrypt
from flask_login import (UserMixin, login_user, LoginManager,current_user, logout_user, login_required)
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import User, Role

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()

app = None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(LocalDevelopmentConfig)
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    return app


app = create_app()
