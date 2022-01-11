from flask import Flask

from config import Config

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import os

# creation of application
app = Flask(__name__)

# connection with the configuration file
app.config.from_object(Config)

# define the database, app.db in root folder
db = SQLAlchemy(app)

# TODO - You are using Migrate. Are you sure you have to
# also have your migrations inside the repo?
migrate = Migrate(app, db)

# starting the login validation process
login = LoginManager(app)

# the LoginManager, named login now, 
# manage the view for user not yet logged in,
#  so they redirect to login page and back after
#  the succesful log, the name 'login' is entering in a url_for
login.login_view = 'login'


bootstrap = Bootstrap(app)

if not app.debug:
    # TODO - Let's leave for now the mail server.
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config('MAIL_USE_TLS'):
            secure = ()
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']), fromaddr='no-reply@' + app.config['MAIL_SERVER'], toaddrs=app.config['ADMINS'], subject='ProgDay Failure', credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler) 
    
    # TODO - use logging without file_handler. On production
    # docker will handle this not flask
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/progday.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # TODO - Maybe the level of logging
    # is good if it was set up according to
    # app.debug
    app.logger.setLevel(logging.INFO)

    # TODO - No need of this for REST
    app.logger.info('ProgDay startup')

# defining the errors blueprint
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

# defining the auth blueprint
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# import the main navigation control for the app
from app import models