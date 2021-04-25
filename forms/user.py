from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    apprentice = StringField('Фамилия пользователя',
                             validators=[DataRequired()])
    patronymic = StringField('Отчество пользователя',
                             validators=[DataRequired()])
    # school = StringField('Отчество пользователя', validators=[DataRequired()])
    # dob = StringField('Дата рождения пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField(
        'Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterDirectorForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    apprentice = StringField('Имя пользователя', validators=[DataRequired()])
    patronymic = StringField('Имя пользователя', validators=[DataRequired()])
    school = StringField('Имя пользователя', validators=[DataRequired()])
    dob = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddStudents(FlaskForm):
    id = StringField('id пользователя', validators=[DataRequired()])
