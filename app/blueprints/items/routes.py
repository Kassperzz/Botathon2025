from flask import render_template
from flask_login import login_required
from . import items_bp

@items_bp.route('/')
@login_required
def list_items():
    return render_template('items/list.html')

@items_bp.route('/<int:item_id>')
@login_required
def item_detail(item_id):
    return render_template('items/detail.html', item_id=item_id)