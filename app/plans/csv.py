import csv
from io import StringIO, BytesIO
from flask import Response
from app.plans.models import MediaPlan

def export_plans_to_csv(plans):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Название', 'Описание', 'Источник', 'Бюджет', 'Дата создания', 'Дата обновления', 'Пользователь'])
    for plan in plans:
        cw.writerow([plan.id, plan.name, plan.description, plan.source, plan.budget, plan.created_at, plan.updated_at, plan.user_id])
    output = si.getvalue()
    si.close()
    return output

def generate_csv_response(plans, filename="media_plans.csv"):
    csv_output = export_plans_to_csv(plans)
    bom = '\ufeff'
    csv_output = bom + csv_output
    response = Response(
        csv_output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
    return response
