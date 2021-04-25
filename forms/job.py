from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, \
    IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class JobForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    team_leader = IntegerField("ID тимлидера", validators=[DataRequired()])
    work_size = IntegerField("Продолжительность", validators=[DataRequired()])
    collaborators = StringField("Участники")
    categories = SelectMultipleField("Категории", coerce=int)
    is_finished = BooleanField("Работа окончена")
    submit = SubmitField("Добавить работу")
