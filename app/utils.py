from functools import wraps
from flask import abort
from flask_login import current_user

# ==========================================
#        DICCIONARIOS DE TRADUCCIÓN
# ==========================================

# 1. Mapa de Regiones (ID -> Nombre)
NOMBRES_REGIONES = {
    1: "Tarapacá", 2: "Antofagasta", 3: "Atacama", 4: "Coquimbo",
    5: "Valparaíso", 6: "O'Higgins", 7: "Maule", 8: "Biobío",
    9: "Araucanía", 10: "Los Lagos", 11: "Aysén", 12: "Magallanes",
    13: "Metropolitana", 14: "Los Ríos", 15: "Arica y Parinacota", 16: "Ñuble"
}

# 2. Lógica de Agrupación de Ocupaciones
CATEGORIAS_OCUPACION = {
    "Estudiantes": ["estud", "alum", "univ", "cursando", "tesista", "pregrado"],
    "Salud": ["enferm", "medic", "kine", "tens", "salud", "nutri", "psico", "terap", "matron", "dentist", "odonto"],
    "Educación": ["profe", "docen", "educ", "pedag", "parvul", "maestr", "academ"],
    "Ingeniería y Tech": ["ing", "inform", "comput", "program", "desarroll", "sistem", "tecni", "mecanic", "electric", "industr"],
    "Administración y Negocios": ["admin", "conta", "secret", "comer", "ventas", "ejecut", "rrhh", "markent", "gesti"],
    "Social y Humanidades": ["social", "trabajador soc", "sociol", "human", "arte", "disen", "comunic", "period"],
    "Fuerzas de Orden": ["carabin", "militar", "ejercito", "armada", "pdi", "segur"],
    "Otros Oficios": ["conduct", "chofer", "cocin", "panad", "const", "gasfit", "vended"]
}

# ==========================================
#           DECORADORES Y ÚTILES
# ==========================================

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Verifica si está autenticado y si tiene el atributo is_admin (o lógica equivalente)
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            return abort(403)
        return f(*args, **kwargs)
    return decorated