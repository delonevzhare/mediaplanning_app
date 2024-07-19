from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from app.user.decorators import admin_required
from app.plans.models import MediaPlan
from collections import defaultdict
from decimal import Decimal

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index():
    if not current_user.is_admin:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('plan.media_plans'))
    
    #Статистика по источникам
    sources_count = defaultdict(int)
    budgets = defaultdict(float)
    plans = MediaPlan.query.all()

    for plan in plans:
        sources_count[plan.source] += 1
        budgets[plan.source] += float(plan.budget)

    source_stats = sorted(sources_count.items())
    budget_stats = sorted(budgets.items())

    title = "Панель управления"
    return render_template('admin/index.html', 
                           page_title=title,
                           source_stats=source_stats,
                           budget_stats=budget_stats)