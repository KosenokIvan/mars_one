from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class DepartmentForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    chief = IntegerField("ID шефа", validators=[DataRequired()])
    members = StringField("Участники")
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField("Добавить департамент")
