import os
from secrets import token_hex

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or token_hex()

    # DB configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
