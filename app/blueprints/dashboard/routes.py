from flask import render_template
from flask_login import login_required, current_user
from . import bp

@bp.route('/')
@login_required
def index():
    # datos de ejemplo para la vista del dashboard
    stats = {"users": 123, "active": 100}
    return render_template('dashboard/index.html', user=current_user, stats=stats)
