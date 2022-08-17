import email
from turtle import title
from application import app,db,bcrypt
from flask import render_template, url_for
from flask import request,flash, redirect
from application.forms import RegistrationForm,LoginForm,CreateList,CreateCard
from application.models import User,List,Card
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime

# @app.before_first_request
# def init_app():
#     logout_user()

@app.route("/board")
@login_required 
def board():
    lists = List.query.all()
    
    return render_template("board.html",lists=lists)

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data,lname=form.lname.data,email=form.email.data,password=hashed_pw)
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
            return redirect(url_for('board'))

        else:
            flash('Login unsuccessful! Please check your credentials again','danger')
    return render_template("signin.html", form=form)


@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    flash('Logout successfully, Try logging in again','success')
    return redirect(url_for('login'))

@app.route("/add_list", methods=["GET","POST"])
@login_required 
def add_list():
    form = CreateList()
    if form.validate_on_submit():
        list = List(name=form.list_name.data,description=form.description.data,user_id=current_user.id)

        checkdblist = List.query.filter_by(name=form.list_name.data).first()
        if not  checkdblist:
            db.session.add(list)
            db.session.commit()
            flash(f'List {form.list_name.data} has been created successfully','success')
            return redirect(url_for('board'))
        else:
            flash(f'List named {form.list_name.data} already exist, Please try again with different name','success')
    return render_template("add_list.html",form=form)

@app.route("/add_card", methods=["GET","POST"])
def add_card():
    form = CreateCard()
    #send list to form choices
    lists = List.query.filter_by(user_id=current_user.id).all()
    form.choose_list.choices = [(list.id,list.name) for list in lists]
    if form.validate_on_submit():
        #check if that cardname exist in that particular list 
        status = False
        complete_status = form.complete_status.data
        if complete_status == 'Completed':
            status = True
        card = Card(title=form.title.data,content=form.content.data,deadline=form.deadline.data,completed_status=status,list_id=form.choose_list.data)
        checkdbcard = Card.query.filter_by(title=form.title.data).first()
        if not checkdbcard:
            db.session.add(card)
            db.session.commit()
            flash(f'List {form.title.data} has been created successfully','success')
            return redirect(url_for('board'))
        else:
            flash(f'Card named "{form.list_name.data}" already exist, Please try again with different name','success')
    return render_template("add_card.html",form=form)


