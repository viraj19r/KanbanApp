from flask_login import UserMixin
from application import login_manager
from datetime import datetime
from application.database import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(), nullable=False)
    lname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    lists = db.relationship('List', backref='user', lazy=True)

    def __repr__(self):
        return f'User-{self.fname} {self.lname}'


class List(db.Model, UserMixin):
    __tablename__ = 'list'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(),nullable=False)
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime(), nullable=False,default=datetime.now())
    # foreign key
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    cards = db.relationship('Card', backref='list', lazy=True)

    def __repr__(self):
        return f'List-{self.name}'


class Card(db.Model, UserMixin):
    __tablename__ = 'card'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(),nullable=False)
    content = db.Column(db.String())
    deadline = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False,default=datetime.now())
    date_completed = db.Column(db.DateTime())
    completed_status = db.Column(db.Boolean(), nullable=False)
    # foreign key
    list_id = db.Column(db.Integer(), db.ForeignKey(
        'list.id',ondelete='CASCADE'))

    def __repr__(self):
        return f'Card-{self.title}'

db.create_all()