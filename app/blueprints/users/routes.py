from flask import render_template
from flask_login import login_required, current_user
from . import users_bp

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)

@users_bp.route('/profile/edit')
@login_required
def profile_edit():
    return render_template('users/profile_edit.html', user=current_user)