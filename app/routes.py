from flask_login.utils import logout_user
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


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