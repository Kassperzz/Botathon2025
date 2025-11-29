# app/blueprints/items/__init__.py
from flask import Blueprint

bp = Blueprint('items', __name__, template_folder='templates')

from app.blueprints.items import routes  # mantiene import de rutas
