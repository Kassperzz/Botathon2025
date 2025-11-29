# app/blueprints/items/routes.py
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Item
from . import bp

@bp.route('/items')
@login_required
def list_items():
    q = request.args.get('q', '')
    if q:
        items = Item.query.filter(Item.name.ilike(f"%{q}%")).order_by(Item.created_at.desc()).all()
    else:
        items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('items/list.html', items=items, q=q)

@bp.route('/items/<int:item_id>')
@login_required
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('items/detail.html', item=item)

@bp.route('/items/create', methods=['GET','POST'])
@login_required
def item_create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('items.item_create'))
        item = Item(name=name, description=description, owner=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Item creado', 'success')
        return redirect(url_for('items.list_items'))
    return render_template('items/form.html', action='Crear', item=None)

@bp.route('/items/<int:item_id>/edit', methods=['GET','POST'])
@login_required
def item_edit(item_id):
    item = Item.query.get_or_404(item_id)
    # permiso: sólo dueño o admin
    if item.owner_id and item.owner_id != current_user.id and not getattr(current_user, 'is_admin', False):
        abort(403)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('items.item_edit', item_id=item.id))
        item.name = name
        item.description = description
        db.session.commit()
        flash('Item actualizado', 'success')
        return redirect(url_for('items.item_detail', item_id=item.id))

    return render_template('items/form.html', action='Editar', item=item)

@bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required
def item_delete(item_id):
    item = Item.query.get_or_404(item_id)
    if item.owner_id and item.owner_id != current_user.id and not getattr(current_user, 'is_admin', False):
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Item eliminado', 'success')
    return redirect(url_for('items.list_items'))
