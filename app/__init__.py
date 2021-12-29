from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)                # creation of application
app.config.from_object(Config)       # connection with the configuration file
db = SQLAlchemy(app)                 # define the database, app.db in root folder
migrate = Migrate(app, db)
login = LoginManager(app)            # starting the login validation process
login.login_view = 'login'           # the LoginManager, named login now, manage the view for user not yet logged in, so they redirect to login page and back after the succesful log, the name 'login' is entering in a url_for

from app import routes               # import the main navigation control for the app