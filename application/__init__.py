from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
# from flask_bcrypt import Bcrypt
# from flask_migrate import Migrate
# from flask_login import (UserMixin,login_user,LoginManager,current_user,logout_user,login_required)


# login_manager = LoginManager()
# login_manager.session_protection = "strong"
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"

# migrate = Migrate()
# bcrypt = Bcrypt()
app = None

def create_app():
    app = Flask(__name__,template_folder='../templates')
    app.config.from_object(LocalDevelopmentConfig)
    # login_manager.init_app(app)
    db.init_app(app)
    # migrate.init_app(app,db)
    # bcrypt.init_app(app)
    app.app_context().push()
    
    return app


app = create_app()


from application.controllers import *