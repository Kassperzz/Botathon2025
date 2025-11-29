from flask import Blueprint

# Definimos el Blueprint
# 'auth' es el nombre que usarás en url_for, ej: url_for('auth.login')
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Importamos las rutas al final
from . import routes