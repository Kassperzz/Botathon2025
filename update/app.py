from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_  # or_ es vital para los filtros de ocupación
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

# 1. INICIALIZAR LA APP
app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Enaxxion13!@127.0.0.1:5432/botathon2025'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura'

db = SQLAlchemy(app)

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
#           MODELOS DE BASE DE DATOS
# ==========================================

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(256))

class Voluntario(db.Model):
    __tablename__ = 'voluntarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150))
    apellido_paterno = db.Column(db.String(100))
    ocupacion = db.Column(db.String(255))
    region_id = db.Column(db.Integer)
    sexo_id = db.Column(db.Integer)
    
    def to_json(self):
        # Traducimos la región al vuelo
        nombre_region = NOMBRES_REGIONES.get(self.region_id, f"Región {self.region_id}")
        return {
            'id': self.id,
            'nombre_completo': f"{self.nombres} {self.apellido_paterno}",
            'ocupacion': self.ocupacion,
            'region': nombre_region
        }

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ==========================================
#           RUTAS DE VISTA (WEB)
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', usuario=current_user.username)

# ==========================================
#           RUTAS DE API (DATOS)
# ==========================================

# Endpoint para llenar el Dropdown de Ocupaciones
@app.route('/api/listas/ocupaciones', methods=['GET'])
@login_required
def lista_ocupaciones():
    # Devolvemos las categorías maestras ordenadas
    return jsonify(sorted(list(CATEGORIAS_OCUPACION.keys())))

# --- FUNCIÓN INTELIGENTE DE FILTROS ---
def aplicar_filtros(query):
    region = request.args.get('region_id')
    sexo = request.args.get('sexo_id')
    categoria = request.args.get('ocupacion')
    
    # 1. Filtro Exacto por Región
    if region and region != "":
        query = query.filter(Voluntario.region_id == int(region))
    
    # 2. Filtro Exacto por Sexo
    if sexo and sexo != "":
        query = query.filter(Voluntario.sexo_id == int(sexo))
        
    # 3. Filtro Lógico por Ocupación (La magia)
    if categoria and categoria in CATEGORIAS_OCUPACION:
        palabras_clave = CATEGORIAS_OCUPACION[categoria]
        # Generamos una lista de condiciones OR (ej: contiene "enf" O contiene "med")
        filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
        query = query.filter(or_(*filtros_or))
        
    return query

@app.route('/api/stats/resumen', methods=['GET'])
@login_required
def obtener_resumen():
    try:
        # 1. Total KPI (Aplica TODOS los filtros seleccionados)
        query_total = aplicar_filtros(Voluntario.query)
        total = query_total.count()
        
        # 2. Desglose Hombres/Mujeres
        # Debemos ignorar el filtro de sexo seleccionado en el dropdown, 
        # pero respetar Región y Ocupación.
        
        base = Voluntario.query
        region = request.args.get('region_id')
        categoria = request.args.get('ocupacion')
        
        if region and region != "":
            base = base.filter(Voluntario.region_id == int(region))
            
        if categoria and categoria in CATEGORIAS_OCUPACION:
            palabras_clave = CATEGORIAS_OCUPACION[categoria]
            filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
            base = base.filter(or_(*filtros_or))
            
        hombres = base.filter(Voluntario.sexo_id == 0).count()
        mujeres = base.filter(Voluntario.sexo_id == 1).count()
        
        return jsonify({
            "total_voluntarios": total,
            "hombres": hombres,
            "mujeres": mujeres
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/por-region', methods=['GET'])
@login_required
def stats_region():
    try:
        query = db.session.query(Voluntario.region_id, func.count(Voluntario.id))
        
        # Filtros Opcionales (Sexo y Ocupación)
        sexo = request.args.get('sexo_id')
        categoria = request.args.get('ocupacion')
        region = request.args.get('region_id') # <--- NUEVO: Capturamos la región
        
        # Si hay una región seleccionada, filtramos la gráfica para mostrar solo esa
        if region and region != "":
            query = query.filter(Voluntario.region_id == int(region))
        
        if sexo and sexo != "":
            query = query.filter(Voluntario.sexo_id == int(sexo))
            
        if categoria and categoria in CATEGORIAS_OCUPACION:
            palabras_clave = CATEGORIAS_OCUPACION[categoria]
            filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
            query = query.filter(or_(*filtros_or))
            
        data = query.group_by(Voluntario.region_id).all()
        
        # Traducimos IDs a Nombres para la gráfica
        resultado = []
        for r in data:
            id_reg = r[0]
            count = r[1]
            if id_reg is not None:
                nombre = NOMBRES_REGIONES.get(id_reg, f"Región {id_reg}")
                resultado.append({"region": nombre, "cantidad": count})
                
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint NUEVO: Estadísticas de Ocupación (Filtradas por Región/Sexo)
@app.route('/api/stats/por-ocupacion', methods=['GET'])
@login_required
def stats_ocupacion():
    try:
        resultado = []
        # Capturamos filtros
        region = request.args.get('region_id')
        sexo = request.args.get('sexo_id')
        
        # Iteramos por nuestras categorías maestras
        for categoria, palabras_clave in CATEGORIAS_OCUPACION.items():
            query = Voluntario.query
            
            # Aplicamos filtros de contexto (Región/Sexo)
            if region and region != "":
                query = query.filter(Voluntario.region_id == int(region))
            if sexo and sexo != "":
                query = query.filter(Voluntario.sexo_id == int(sexo))
                
            # Filtro específico de la categoría (OR ILIKE)
            filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
            cantidad = query.filter(or_(*filtros_or)).count()
            
            resultado.append({"categoria": categoria, "cantidad": cantidad})
            
        # Ordenamos de mayor a menor
        resultado = sorted(resultado, key=lambda x: x['cantidad'], reverse=True)
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/voluntarios', methods=['GET'])
@login_required
def obtener_voluntarios():
    lista = Voluntario.query.limit(50).all()
    return jsonify([v.to_json() for v in lista])

if __name__ == '__main__':
    app.run(debug=True)