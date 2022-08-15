import email
from application import app,db,bcrypt
from flask import render_template, url_for
from flask import request,flash, redirect
from application.forms import RegistrationForm,LoginForm
from application.models import User
from flask_login import login_user,logout_user,login_required


# @app.before_first_request
# def init_app():
#     logout_user()

@app.route("/")
@login_required
def hello():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data,lname=form.lname.data,email=form.email.data,password=hashed_pw,active=True)
        db.session.add(user)
        db.session.commit()
        flash(f'Hii {form.fname.data}! Your account has been created. You can login now','success')
        return redirect(url_for('login'))
    return render_template("register.html",form=form)
        

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('hello'))

        else:
            flash('Login unsuccessful! Please check your credentials again','danger')
    return render_template("signin.html", form=form)


@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    flash('Logout successfully, Try logging in again','success')
    return redirect(url_for('login'))
