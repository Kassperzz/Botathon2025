from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.extensions import db, login_manager
from app.models import User
from . import bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next') or url_for('dashboard.index')
            return redirect(next_page)
        flash('Credenciales inválidas', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email ya registrado', 'warning')
            return redirect(url_for('auth.register'))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada, ya puedes entrar', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
