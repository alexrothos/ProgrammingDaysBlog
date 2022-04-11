from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from flask_login import UserMixin

from app import db, login


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)


class User(BaseModel, UserMixin):
    __tablename__ = 'user_table'

    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())
    user_posts = db.relationship('Post', cascade="all,delete", backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_name(cls, _username):
        return cls.query.filter_by(username=_username).first()
        
    def serialize(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'password':self.password_hash,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(BaseModel):
    __tablename__ = 'post_table'

    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), on_delete)
    title = db.Column(db.String(150))
    body = db.Column(db.String(340))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    @classmethod
    def find_by_user_id(cls, _user_id):
        return cls.query.filter_by(user_id=_user_id).all()

    def serialize(self):
        return {
            'id':self.id,
            'user_id':self.user_id,
            'title':self.title,
            'body':self.body,
            'timestamp':self.timestamp
        }

# @classmethod - TODO what is a class method?
# def find_by_id(self, id) # this will be applied to every model -> Post.find_by_id()