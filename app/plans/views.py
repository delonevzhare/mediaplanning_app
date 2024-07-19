from flask import Blueprint, Response, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user

from app.plans.models import MediaPlan
from app.plans.forms import MediaPlanForm
from app.db import db

import csv
import logging
from io import StringIO, BytesIO
import zipfile

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

@blueprint.route('/process_plans', methods=['POST'])
@login_required
def process_plans():
    data = request.form
    plan_numbers = data.getlist('plan_numbers')

    if not plan_numbers:
        flash('Пожалуйста, выберите медиаплан.', 'warning')
        return redirect(url_for('plan.media_plans'))

    if 'csv' in data:
        return download_csv(plan_numbers)
    elif 'delete' in data:
        return delete_plans(plan_numbers)
    else:
        flash('Некорректное действие.', 'danger')
        return redirect(url_for('plan.media_plans'))

def delete_plans(plan_numbers):
    logging.info(f"Received plan numbers: {plan_numbers}")
    plans_to_delete = MediaPlan.query.filter(MediaPlan.plan_number.in_(plan_numbers), MediaPlan.user_id == current_user.id).all()
    logging.info(f"Plans to delete: {plans_to_delete}")
    if not plans_to_delete:
        flash('Медиапланы не найдены или у вас нет доступа к ним.', 'danger')
        return redirect(url_for('plan.media_plans'))

    for plan in plans_to_delete:
        db.session.delete(plan)
    db.session.commit()
    logging.info("Plans deleted successfully.")
    flash('Выбранные медиапланы успешно удалены.', 'success')
    return redirect(url_for('plan.media_plans'))

def download_csv(plan_numbers):
    plans = MediaPlan.query.filter(MediaPlan.plan_number.in_(plan_numbers), MediaPlan.user_id == current_user.id).all()
    if not plans:
        flash('Медиапланы не найдены или у вас нет доступа к ним.', 'danger')
        return redirect(url_for('plan.media_plans'))

    # Export plans to CSV
    def export_plans_to_csv(plans):
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['ID', 'Название', 'Описание', 'Источник', 'Бюджет', 'Дата создания', 'Дата обновления', 'Пользователь'])
        for plan in plans:
            cw.writerow([plan.id, plan.name, plan.description, plan.source, plan.budget, plan.created_at, plan.updated_at, plan.user_id])
        output = si.getvalue()
        si.close()
        return output

    if len(plans) == 1:
        csv_output = export_plans_to_csv(plans)
        bom = '\ufeff'  # Добавляем BOM для корректного отображения в Excel
        csv_output = bom + csv_output
        response = Response(
            csv_output,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename=media_plan_{plans[0].plan_number}.csv"}
        )
        return response
    else:
        def generate_zip_response(plans):
            csv_output = export_plans_to_csv(plans)
            bom = '\ufeff'
            csv_output = bom + csv_output

            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr('media_plans.csv', csv_output)
            
            zip_buffer.seek(0)
            return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='media_plans.zip')
        
        return generate_zip_response(plans)