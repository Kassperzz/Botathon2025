from flask import jsonify, request
from flask_login import login_required
from sqlalchemy import func, or_
from app.extensions import db
from app.models import Voluntario
from app.utils import CATEGORIAS_OCUPACION, NOMBRES_REGIONES
from . import api_bp

# --- HELPER FILTROS ---
def aplicar_filtros(query):
    region = request.args.get('region_id')
    sexo = request.args.get('sexo_id')
    categoria = request.args.get('ocupacion')
    
    if region and region != "":
        query = query.filter(Voluntario.region_id == int(region))
    if sexo and sexo != "":
        query = query.filter(Voluntario.sexo_id == int(sexo))
    if categoria and categoria in CATEGORIAS_OCUPACION:
        palabras_clave = CATEGORIAS_OCUPACION[categoria]
        filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
        query = query.filter(or_(*filtros_or))
    return query

# --- RUTAS ---
@api_bp.route('/listas/ocupaciones', methods=['GET'])
@login_required
def lista_ocupaciones():
    return jsonify(sorted(list(CATEGORIAS_OCUPACION.keys())))

@api_bp.route('/stats/resumen', methods=['GET'])
@login_required
def obtener_resumen():
    try:
        # Total KPI
        query_total = aplicar_filtros(Voluntario.query)
        total = query_total.count()
        
        # Desglose Hombres/Mujeres (ignorando filtro sexo)
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
        
        return jsonify({"total_voluntarios": total, "hombres": hombres, "mujeres": mujeres})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/stats/por-region', methods=['GET'])
@login_required
def stats_region():
    try:
        query = db.session.query(Voluntario.region_id, func.count(Voluntario.id))
        
        # Filtros manuales para grouping
        sexo = request.args.get('sexo_id')
        categoria = request.args.get('ocupacion')
        region = request.args.get('region_id')
        
        if region and region != "":
            query = query.filter(Voluntario.region_id == int(region))
        if sexo and sexo != "":
            query = query.filter(Voluntario.sexo_id == int(sexo))
        if categoria and categoria in CATEGORIAS_OCUPACION:
            palabras_clave = CATEGORIAS_OCUPACION[categoria]
            filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
            query = query.filter(or_(*filtros_or))
            
        data = query.group_by(Voluntario.region_id).all()
        resultado = []
        for r in data:
            id_reg = r[0]
            if id_reg is not None:
                nombre = NOMBRES_REGIONES.get(id_reg, f"Región {id_reg}")
                resultado.append({"region": nombre, "cantidad": r[1]})
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/stats/por-ocupacion', methods=['GET'])
@login_required
def stats_ocupacion():
    try:
        resultado = []
        region = request.args.get('region_id')
        sexo = request.args.get('sexo_id')
        
        for categoria, palabras_clave in CATEGORIAS_OCUPACION.items():
            query = Voluntario.query
            if region and region != "":
                query = query.filter(Voluntario.region_id == int(region))
            if sexo and sexo != "":
                query = query.filter(Voluntario.sexo_id == int(sexo))
            filtros_or = [Voluntario.ocupacion.ilike(f"%{palabra}%") for palabra in palabras_clave]
            cantidad = query.filter(or_(*filtros_or)).count()
            resultado.append({"categoria": categoria, "cantidad": cantidad})
            
        return jsonify(sorted(resultado, key=lambda x: x['cantidad'], reverse=True))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/voluntarios', methods=['GET'])
@login_required
def obtener_voluntarios():
    lista = Voluntario.query.limit(50).all()
    return jsonify([v.to_json() for v in lista])