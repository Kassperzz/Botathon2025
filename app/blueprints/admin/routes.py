from flask import render_template
from flask_login import login_required
from ...models import User
from ...utils import admin_required   # donde pusiste el decorator
from . import bp

@bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.limit(50).all()
    return render_template('admin/index.html', users=users)
