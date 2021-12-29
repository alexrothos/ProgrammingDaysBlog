from flask_login.utils import logout_user
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required                                     # to protect the function to be used without validation
def index():
    posts = []
    return render_template("index.html", title='Home page of Programming Days Blog', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged, redirecting to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
        # here starts the handling for the "next" in url /login?next=/index query
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # securing with url_parse the redirect
            next_page = url_for('index')
        
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # setting the user's data in place
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # adding the new user to the database
        db.session.add(user)
        db.session.commit()

        flash('Registration succeful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Student Registration', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = []
    return render_template('user.html', user=user, posts=posts)

# here is the time registration of users
@app.before_request     # the before_request is to be executed right before any request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() # the current_user is already loaded, so no need to add to db
        db.session.commit() # the db.session.add is unecessary

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)