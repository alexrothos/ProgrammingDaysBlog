import os
from secrets import token_hex

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or token_hex()

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
