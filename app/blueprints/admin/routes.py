from flask import render_template
from flask_login import login_required
from . import admin_bp

@admin_bp.route('/')
@login_required
def index():
    # Aquí iría lógica solo para administradores
    return render_template('admin/index.html')