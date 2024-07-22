from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.user.decorators import admin_required
from app.user.models import User
from app.db import db
from app.admin.forms import UserForm

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    form = UserForm()
    users = User.query.all()
    user_id = request.args.get('user_id')

    if request.method == 'POST' and form.validate_on_submit():
        if user_id:
            user = User.query.get_or_404(user_id)
            form.populate_obj(user)
            flash('Пользователь успешно обновлен!', 'success')
        else:
            new_user = User(username=form.username.data, email=form.email.data, role=form.role.data)
            db.session.add(new_user)
            flash('Пользователь успешно добавлен!', 'success')
        db.session.commit()
        return redirect(url_for('admin.manage_users'))

    if user_id:
        user = User.query.get_or_404(user_id)
        form = UserForm(obj=user)
        form.user_id.data = user.id

    return render_template('admin/manage_users.html', users=users, form=form)

@blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('admin.manage_users'))

