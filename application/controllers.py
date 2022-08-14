from application.__init__ import app
from flask import render_template, url_for
from flask import request,flash, redirect
from application.forms import RegistrationForm,LoginForm

@app.route("/")
def hello():
    return render_template("signin.html", index="viraj")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.fname.data} {form.lname.data} successfully','success')
        return redirect(url_for('index.html'))
    return render_template("register.html",form=form)
        

@app.route("/signin", methods=["GET","POST"])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.email.data} logged in successfully!','success')
        return redirect(url_for('register'))
    return render_template("signin.html", form=form)
