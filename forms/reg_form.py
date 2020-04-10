# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """Класс формы для регистрации пользователя"""
    login = StringField('Логин', validators=[DataRequired(message='Обязательное поле')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Обязательное поле')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message='Обязательное поле')])
    surname = StringField('Фамилия', validators=[DataRequired(message='Обязательное поле')])
    name = StringField('Имя', validators=[DataRequired(message='Обязательное поле')])
    age = IntegerField('Возраст', validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Зарегистрироваться')
