from ast import Pass
from sqlite3 import Date
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from sqlalchemy import false
from application import app
from wtforms import StringField,PasswordField,SubmitField,SelectField,TextAreaField,DateField,RadioField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from wtforms.widgets.html5 import DateInput
from application.models import User


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(),Length(min=2, max=25)])
    lname = StringField('Last Name',validators=[DataRequired(),Length(min=2, max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    #custom validations
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please try with another one')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class CreateList(FlaskForm):
    list_name = StringField('List Name',validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Save')
    

class CreateCard(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    deadline = DateField('Deadline  :',validators=[DataRequired()],widget=DateInput())
    choose_list = SelectField('Lists  :',choices=[],coerce=int)
    complete_status = SelectField('Status  :',choices=[('Uncompleted','Uncompleted'),('Completed','Completed')])
    submit = SubmitField('Save')

class MoveCardDeleteList(FlaskForm):
    choose_list = SelectField('Move cards to this list  :',choices=[],coerce=int)
    submit = SubmitField('Delete the List')




