from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.plans.models import MediaPlan
from app.plans.forms import MediaPlanForm
from app.plans.csv import generate_csv_response
from app.db import db

blueprint = Blueprint('plan', __name__, url_prefix='/media_plans')

@blueprint.route('/')
@login_required
def media_plans():
    plans = MediaPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('plans/media_plans.html', media_plans=plans)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_media_plan():
    form = MediaPlanForm()
    if form.validate_on_submit():
        max_plan_number = db.session.query(db.func.max(MediaPlan.plan_number)).filter_by(user_id=current_user.id).scalar() or 0
        new_plan_number = max_plan_number + 1

        new_plan = MediaPlan(
            name=form.name.data,
            description=form.description.data,
            source=form.source.data,
            budget=form.budget.data,
            user_id=current_user.id,
            plan_number=new_plan_number
        )
        db.session.add(new_plan)
        db.session.commit()
        flash('Медиаплан успешно создан!', 'success')
        return redirect(url_for('plan.media_plans'))
    return render_template('plans/create_media_plan.html', form=form, page_title="Создание медиаплана")

@blueprint.route('/download_csv')
@login_required
def download_csv():
    plans = MediaPlan.query.filter_by(user_id=current_user.id).all()
    return generate_csv_response(plans)

