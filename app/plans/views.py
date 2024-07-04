from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.plans.models import MediaPlan
from app.plans.forms import MediaPlanForm
from app import db

blueprint = Blueprint('plan', __name__)

@blueprint.route('/')
def index():
    title = "Сервис медиапланирования"
    return render_template('index.html', page_title=title)

@blueprint.route('/media_plans')
@login_required
def media_plans():
    # Получение медиапланов текущего пользователя
    plans = MediaPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('plans/media_plans.html', media_plans=plans)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_media_plan():
    form = MediaPlanForm()
    if form.validate_on_submit():
        new_plan = MediaPlan(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_plan)
        db.session.commit()
        flash('Медиаплан успешно создан!', 'success')
        return redirect(url_for('plan.media_plans'))
    
    return render_template('plans/create_media_plan.html', form=form, page_title="Создание медиаплана")
