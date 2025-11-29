# app/blueprints/users/__init__.py
from flask import Blueprint
bp = Blueprint('users', __name__, template_folder='templates')
from app.blueprints.users import routes
