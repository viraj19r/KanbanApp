from enum import unique
from application.database import db
from flask_security import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
