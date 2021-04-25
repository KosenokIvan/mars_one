from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed


class GalleryForm(FlaskForm):
    image = FileField("Добавить картинку", validators=[FileAllowed(["png", "jpg", "jpeg"])])
    submit = SubmitField("Добавить картинку")
