from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.user.models import User
from app.user.forms import LoginForm, RegistrationForm
from app.db import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user_name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неправильные имя или пароль', 'danger')
    title = "Авторизация"
    return render_template('user/login.html', page_title=title, form=form)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно разлогинились', 'success')
    return redirect(url_for('main.index'))

@blueprint.route('/registration', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.user_name.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('user.login'))
    title = "Регистрация"
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.user_name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт', 'success')
            return redirect(url_for('main.index'))
        
        flash('Неправильные имя или пароль', 'danger')
        return redirect(url_for('user.login'))
    return render_template('user/login.html', form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.user_name.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('user.login'))
    flash('Пожалуйста, исправьте ошибки в форме', 'danger')
    return render_template('user/registration.html', form=form)
