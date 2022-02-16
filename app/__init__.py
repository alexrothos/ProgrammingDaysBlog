from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT

from config.config import Config



"""
app/__init__.py
    --> creates app(flask), db(sqlalchemy),
        migrate(automatic migrations with alembic)
    --> from app import error, auth
        
    **  For example if you want a route only for debugging
        you can imported only if app.debug == True

app/routes.py ****(you have to create this file)
    inside it
        from app import auth
    
    --> this goes to app/auth/__init__.py

app/auth/__init__.py ****(you have to create this file)
    inside it
        from .auth import routes

    --> this will import every method inside
        app/auth/routes.py
"""

# creation of application
app = Flask(__name__)

# connection with the configuration file
app.config.from_object(Config)

# define the database, app.db in root folder
db = SQLAlchemy(app)

from app.auth.security import authenticate, identity
jwt = JWT(app, authenticate, identity)

# TODO - You are using Migrate. Are you sure you have to
# also have your migrations inside the repo?
migrate = Migrate(app, db)

from app import auth, post