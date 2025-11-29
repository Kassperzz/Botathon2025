# app/blueprints/users/routes.py
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User
from . import bp

@bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)

@bp.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Perfil actualizado', 'success')
        return redirect(url_for('users.profile'))
    return render_template('users/profile_edit.html', user=current_user)
