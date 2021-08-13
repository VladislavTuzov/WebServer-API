from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired


class UpLoadForm(FlaskForm):
    name = StringField('Название позиции', validators=[DataRequired()])
    description = TextAreaField(
        'Введите описание', validators=[DataRequired()])
    price = StringField('Введите цену', validators=[DataRequired()])
    weight = StringField('Введите вес', validators=[DataRequired()])
    image = FileField('Your photo', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddCupons(FlaskForm):
    coupon = StringField('Введите код купона', validators=[DataRequired()])
    description = TextAreaField(
        'Введите описание', validators=[DataRequired()])
    discount = IntegerField('Введите скидку', validators=[DataRequired()])
    id_klient = IntegerField(
        'id пользователя для которого этот купон', validators=[DataRequired()])
    submit = SubmitField('Добавить')
