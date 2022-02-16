from app.models import User


def authenticate(username, password):
    user = User.query.filter_by(username).first()
    if user and User.check_password(user.password_hash, password):
        return user
    else:
        return None

def identity(payload):
    user_id = payload['identity']
    return User.find_user_by_id(user_id)