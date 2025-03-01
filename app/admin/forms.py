from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    user_id = HiddenField()
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"id": "form-username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"id": "form-email"})
    role = SelectField('Роль', choices=[('user', 'Пользователь'), ('admin', 'Администратор')], validators=[DataRequired()], render_kw={"id": "form-role"})
    submit = SubmitField('Добавить', render_kw={"id": "form-submit"})

