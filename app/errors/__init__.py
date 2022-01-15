from flask import Blueprint

# creation of Blueprint class with the
# folder definition 'errors'
bp = Blueprint('errors', __name__)

# this line loads to app the classes handlers.py
# has for error managing
from app.errors import handlers