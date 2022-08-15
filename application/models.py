from enum import unique
from flask_login import UserMixin
from application import login_manager
from application.database import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(),primary_key=True)
    fname = db.Column(db.String(),nullable=False)
    lname = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    active = db.Column(db.Boolean())


# class RolesUsers(db.Model):
#     __tablename__ = 'roles_users'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))




    def __repr__(self):
        return f'{self.fname}{self.lname}'

# class Role(db.Model, RoleMixin):
#     __tablename__ = 'role'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))


