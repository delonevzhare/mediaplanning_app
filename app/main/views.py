from flask import Blueprint, render_template
from flask_login import current_user
from app.plans.models import MediaPlan

blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def index():
    plan_count = 0
    if current_user.is_authenticated:
        plan_count = MediaPlan.query.filter_by(user_id=current_user.id).count()
    return render_template('main.html', plan_count=plan_count)

