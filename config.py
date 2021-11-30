import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'knowledge-is-the-key'

    # Mail configuration
    MAIL_SERVER = os.environ.get('???')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('???')
    MAIL_PASSWORD = os.environ.get('???')
    
    # Misc configurations
    ADMINS = ['alexrothos@gmail.com']

    # DB configuration