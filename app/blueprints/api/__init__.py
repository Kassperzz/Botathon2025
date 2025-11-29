from flask import Blueprint

# Definimos el Blueprint
api_bp = Blueprint('api', __name__)

# Importamos las rutas al final
from . import routes