from poplib import POP3_SSL_PORT
from turtle import update
from unittest import result
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from app import db

#class BaseModel(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
    # TODO - Define __schema__ class
    # TODO - Create base model and inheritt to all models
    # id is a common field for every new model. You don't
    # have to create it every time.



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def find_user_by_name(username):
        user = User.query.filter_by(username=username).first()
        result = {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password_hash
        }
        return result

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    body = db.Column(db.String(340))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    # TODO create a method find_by_user_id which will select posts only for this user
    # DONE ? for this user
    def find_by_id(find_id):
        post = Post.query.filter_by(id=find_id).first()
        result = {
            'id':post.id,
            'user_id':post.user_id,
            'title':post.title,
            'body':post.body,
            'timestamp':post.timestamp
        }
        return result

    def find_by_user_id(self):
        posts_by_user = Post.query.filter_by(user_id=self.user_id)
        return posts_by_user

    def all_posts():
        result = []
        posts = Post.query.all()
        for post in posts:
            {
                "id":post.id,
                "title":post.title,
                "body":post.body,
                "user_id":post.user_id,
                "timestamp":post.timestamp
            }
            result.append(post)

        return {"posts":result}

# TODO - create a base class - BaseModel which will be inherited by all your models
# for example class Post(BaseModel)
# class BaseModel(db.Model):
    # id = db.Column(db.Integer, primary_key=True) # Every model has an id you don't have to use them all the time

    # @classmethod - TODO what is a class method?
    # def find_by_id(self, id) # this will be applied to every model -> Post.find_by_id()