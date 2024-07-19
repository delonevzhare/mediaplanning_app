from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired

class MediaPlanForm(FlaskForm):
    name = StringField('Название медиаплана', validators=[DataRequired()])
    source = SelectField('Источник', choices=[
        ('Yandex.Direct', 'Яндекс.Директ'),
        ('VKontakte', 'VKontakte'),
        ('Telegram', 'Telegram')
    ], validators=[DataRequired()])
    budget = DecimalField('Бюджет', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Создать')
