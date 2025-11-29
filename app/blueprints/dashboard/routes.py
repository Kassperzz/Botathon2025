from flask import render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
from . import dashboard_bp
from app.utils import NOMBRES_REGIONES  # <-- importar la constante

@dashboard_bp.route('/')
def index():
    # Redirigir a login si entra a la raíz
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
@login_required
def home():
    return render_template(
        'dashboard/index.html',
        usuario=current_user.username,
        NOMBRES_REGIONES=NOMBRES_REGIONES  # <-- pasar al template
    )

@dashboard_bp.route('/logout')
def logout_redirect():
    # Opcional: Cerrar sesión aquí también por seguridad antes de redirigir
    logout_user() 
    return redirect(url_for('auth.login'))
