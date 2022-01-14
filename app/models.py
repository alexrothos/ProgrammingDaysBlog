from datetime import datetime

from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from hashlib import md5

followers = db.Table('followers', db.Column('follower_id',\
     db.Integer, db.ForeignKey('user.id')),db.Column('followed_id',\
          db.Integer, db.ForeignKey('user.id')))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    # TODO - Define __schema__ class
    # TODO - Create base model and inheritt to all models
    # id is a common field for every new model. You don't
    # have to create it every time.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User', secondary=followers, \
        primaryjoin=(followers.c.follower_id == id), secondaryjoin=(\
            followers.c.followed_id == id), backref=db.backref('followers',\
                 lazy='dynamic'), lazy='dynamic')
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # TODO - put repr right after the variables.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # this is the Avatar method to create a unique avatar 
    # with Gravatar service, it can be changed in the future though
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.\
            format(digest, size)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    # TODO - Maybe you have to create find_by_id method? To find a user in db?

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), required=True)
    body = db.Column(db.String(340))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # TODO - ids-foreign_keys then all the other attributes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    # TODO create a method find_by_user_id which will select posts only for this user

# TODO - create a base class - BaseModel which will be inherited by all your models
# for example class Post(BaseModel)
# class BaseModel(db.Model):
    # id = db.Column(db.Integer, primary_key=True) # Every model has an id you don't have to use them all the time

    # @classmethod - TODO what is a class method?
    # def find_by_id(self, id) # this will be applied to every model -> Post.find_by_id()