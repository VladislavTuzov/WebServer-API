from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired


class UploadAvatar(FlaskForm):
    fileName = FileField()
    submit = SubmitField('Загрузить')
