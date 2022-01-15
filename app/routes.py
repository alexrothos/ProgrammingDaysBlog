from email.quoprimime import body_check
from turtle import title
from flask_login.utils import logout_user

from flask import render_template, flash, redirect, url_for, request, jsonify

from flask_login import current_user, login_user, \
    logout_user, login_required

from app import app, db

from app.models import User, Post

from app.forms import LoginForm, RegistrationForm, \
    EditProfileForm, EmptyForm, PostForm

from werkzeug.urls import url_parse

from datetime import datetime


@app.route('/post', methods=['GET','POST', 'PUT'])
@login_required
def manage_post():
    if request.method in ['POST', 'PUT']:
        # GET object supposed not to have a body.
        # The same with delete
        try:
            data = request.get_data()
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Bad request or lost data'
            })
        if data:
            # Gets field from body - title and body
            title = data.get('title', None)
            body = data.get('body', None)
            if request.method == 'POST':
                # If request is post creates a new object
                post = Post(title=title, body=body)
            elif request.method == 'PUT':
                # If request is put/patch updates an existing object
                # so you have to send an id in body
                # TODO return error response "request failed" when post not exist
                post_id = data.get('post_id')
                post = Post.find_by_id(post_id)
                post.title = title
                post.body = body
            try:
                # always try before commiting to database
                db.session.commit()
            except Exception as e:
                # whenever something gets wrong with save rollback (undo)
                db.session.rollback()
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': str(e)
                })
            return jsonify({
                'error': False,
                'code': 200,
                'title': 'Post saved',
                'msg': 'Post saved'
            })
        # No data means something broke with the request
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Something went wrong. Please try again later'
            })
    # elif request.method == 'DELETE'
    # TODO add a delete method
    else: # request is GET
        # TODO find how to get a specific post with GET /post/{id}
        # TODO find how to fetch user_id from login_required
        posts = Post.find_by_user_id(user_id)
        # TODO learn more about how to use marshmellow for making a model -> json
        # TODO you have to return a list of posts in json

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
        
        # here starts the handling for the "next" in url 
        # /login?next=/index query
        next_page = request.args.get('next')
        # securing with url_parse the redirect
        if not next_page or url_parse(next_page).netloc != '':
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
    return render_template('register.html', title='Student Registration',\
         form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, \
        app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,\
         next_url=next_url, prev_url=prev_url, form=form)

# here is the time registration of users
# the before_request is to be executed right before any request
@app.before_request     
def before_request():
    if current_user.is_authenticated:
        # the current_user is already loaded, so no need to add to db
        current_user.last_seen = datetime.utcnow()
        # the db.session.add is unecessary 
        db.session.commit() 

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',\
         form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc())\
        .paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore',\
         posts=posts.items,next_url=next_url, prev_url=prev_url)