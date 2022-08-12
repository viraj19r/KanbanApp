import os

basedir = os.path.abspath(os.path.dirname(__file__))

class LocalDevelopmentConfig():
    sqlite_db_dir = os.path.join(basedir, "../db_folder")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(sqlite_db_dir,"test.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = 'my-secret-key'
    SECURITY_PASSWORD_SALT	= 'salt-key'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTRABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None