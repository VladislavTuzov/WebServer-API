from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddSchoolsForm(FlaskForm):
    name = StringField('Название школы', validators=[DataRequired()])
    # id = StringField('id пользователя', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class AddKlass(FlaskForm):
    name = StringField('Название класса', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
