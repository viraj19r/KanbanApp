import email
from os import stat
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
    return render_template("board.html",user=current_user)

@app.route("/summary")
@login_required 
def summary():
    lists = List.query.all()
    return render_template("summary.html",user=current_user)


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
@login_required 
def logout():
    logout_user()
    flash('Logout successfully, Try logging in again','success')
    return redirect(url_for('login'))

@app.route("/add_list", methods=["GET","POST"])
@login_required 
def add_list():
    form = CreateList()
    all_lists = List.query.all()
    if len(all_lists) < 5 :
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
    else:
            flash(f'You cannot create more than 5 Lists','warning')
            return redirect(url_for('board'))
    return render_template("add_list.html",form=form)

@app.route("/add_card", methods=["GET","POST"])
@login_required
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
            flash(f'Card {form.title.data} has been created successfully','success')
            return redirect(url_for('board'))
        else:
            flash(f'Card named "{form.title.data}" already exist, Please try again with different name','success')
    return render_template("add_card.html",form=form)

@app.route("/edit_list/<int:list_id>", methods=["GET","POST"])
@login_required 
def edit_list(list_id):
    form = CreateList()
    list = List.query.filter_by(id=list_id).first()
    if request.method == 'GET':
        form.list_name.data = list.name
        form.description.data = list.description
    if form.validate_on_submit():
        checkdblist = List.query.filter_by(name=form.list_name.data).first()
        if not  checkdblist:
            list.name = form.list_name.data
            list.description = form.description.data
            db.session.commit()
            flash(f'List updated successfully','success')
            return redirect(url_for('board'))
        else:
            flash(f'List named {form.list_name.data} already exist, Please try again with different name','success')
    return render_template("edit_list.html",form=form)

@app.route("/edit_card/<int:card_id>", methods=["GET","POST"])
@login_required
def edit_card(card_id):
    form = CreateCard()
    #send list to form choices
    lists = List.query.filter_by(user_id=current_user.id).all()
    form.choose_list.choices = [(list.id,list.name) for list in lists]
    card = Card.query.filter_by(id=card_id).first()
    if request.method == "GET":
        form.title.data = card.title
        form.content.data = card.content
        form.deadline.data = card.deadline
    if form.validate_on_submit():
        status = False
        complete_status = form.complete_status.data
        if complete_status == 'Completed':
            status = True
        #check if that cardname exist in that particular list 
        checkdbcard = Card.query.filter_by(title=form.title.data)
        checkdbcard = [c for c in checkdbcard if c!=card]
        if not checkdbcard:
            card.title = form.title.data
            card.content = form.content.data
            card.deadline = form.deadline.data
            card.completed_status = status
            card.list_id = form.choose_list.data
            db.session.commit()
            flash(f'Card updated successfully','success')
            return redirect(url_for('board'))
        else:
            flash(f'Card named "{form.title.data}" already exist, Please try again with different name','success')
    return render_template("edit_card.html",form=form)

@app.route("/delete_list/<int:list_id>", methods=["GET","POST"])
@login_required 
def delete_list(list_id):
    list = List.query.filter_by(id=list_id).first()
    list_name = list.name
    cards = list.cards
    for card in cards:
        db.session.delete(card)
    db.session.delete(list)
    db.session.commit()
    flash(f'List named {list_name} deleted successfully','success')
    return redirect(url_for('board'))


@app.route("/delete_card/<int:card_id>", methods=["GET","POST"])
@login_required
def delete_card(card_id):
    card = Card.query.filter_by(id=card_id).first()
    card_title = card.title
    db.session.delete(card)
    db.session.commit()
    flash(f'Card {card_title} deleted successfully','success')
    return redirect(url_for('board'))



@app.route("/mark_card_completed/<int:card_id>", methods=["GET","POST"])
@login_required
def mark_card_completed(card_id):
    card = Card.query.filter_by(id=card_id).first()
    card_title = card.title
    card.completed_status = True
    card.date_completed = datetime.now()
    db.session.commit()
    flash(f'Card "{card_title}" marked as completed','success')
    return redirect(url_for('board'))


