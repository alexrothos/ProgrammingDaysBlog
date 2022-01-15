from flask import Blueprint

# creation of Blueprint class with the
# folder definition 'auth'
bp = Blueprint('auth', __name__)

# this line loads to app the classes from routes.py
from app.auth import routes