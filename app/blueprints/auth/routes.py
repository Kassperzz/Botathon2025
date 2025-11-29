from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

# Importamos el modelo Admin (Asegúrate de tener models.py en app/)
from app.models import Admin
# Importamos el blueprint que acabamos de definir en el __init__
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Si el usuario ya está logueado, lo mandamos directo al Dashboard
    if current_user.is_authenticated:
        # Nota: 'dashboard.home' asume que en dashboard/routes.py definiste la función como 'home'
        return redirect(url_for('dashboard.home'))

    # 2. Procesamos el formulario
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Buscamos al admin en la base de datos
        admin = Admin.query.filter_by(username=username).first()
        
        # Verificamos contraseña
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            # Redirigimos al Dashboard tras éxito
            return redirect(url_for('dashboard.home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            
    # 3. Si es GET o falló el login, mostramos el formulario
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has salido de la plataforma", "info")
    return redirect(url_for('auth.login'))
