# app/blueprints/api/routes.py
from flask import jsonify
from app.models import User
from . import bp

@bp.route('/status')
def status():
    return jsonify({"status": "ok"})

@bp.route('/users')
def list_users():
    users = User.query.limit(50).all()
    return jsonify([{"id": u.id, "email": u.email} for u in users])
