from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from flask_login import UserMixin

from app import db, login

class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def find_by_id(self, id):
        result = Post.query.filter_by(id=id).first()
        if not result:
            return None
        return result

    # TODO - Define __schema__ class
    # TODO - Create base model and inheritt to all models
    # id is a common field for every new model. You don't
    # have to create it every time.



class User(UserMixin, db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True)
    user_posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def find_user_by_name(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None
        result = {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password_hash,
            'created_at':user.created_at,
            'updated_at':user.updated_at
        }
        return result
    
    def find_user_by_id(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return None
        result = {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password_hash,
            'created_at':user.created_at,
            'updated_at':user.updated_at
        }
        return result

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'post_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    title = db.Column(db.String(150))
    body = db.Column(db.String(340))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def find_by_user(username):
        user_id = User.find_user_by_name(username)['id']
        post_q = Post.query.filter_by(user_id=user_id).all()
        posts = []
        for post in post_q:
            result = {
                'id':post.id,
                'user_id':post.user_id,
                'title':post.title,
                'body':post.body,
                'timestamp':post.timestamp
                }
            posts.append(result)
        return {'posts':posts}

    def find_by_id(post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return None
        return post


# TODO - create a base class - BaseModel which will be inherited by all your models
# for example class Post(BaseModel)
# class BaseModel(db.Model):
# # id = db.Column(db.Integer, primary_key=True) # Every model has an id you don't have to use them all the time

# @classmethod - TODO what is a class method?
# def find_by_id(self, id) # this will be applied to every model -> Post.find_by_id()