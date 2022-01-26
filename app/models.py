from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    # TODO - Define __schema__ class
    # TODO - Create base model and inheritt to all models
    # id is a common field for every new model. You don't
    # have to create it every time.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # TODO - put repr right after the variables.

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(340))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    # TODO create a method find_by_user_id which will select posts only for this user

# TODO - create a base class - BaseModel which will be inherited by all your models
# for example class Post(BaseModel)
# class BaseModel(db.Model):
    # id = db.Column(db.Integer, primary_key=True) # Every model has an id you don't have to use them all the time

    # @classmethod - TODO what is a class method?
    # def find_by_id(self, id) # this will be applied to every model -> Post.find_by_id()