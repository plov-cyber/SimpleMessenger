# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    """Класс формы для редактирования профиля"""
    surname = StringField('Фамилия', validators=[DataRequired(message='Введите фамилию')])
    name = StringField('Имя', validators=[DataRequired(message='Введите имя')])
    age = IntegerField('Возраст', validators=[DataRequired(message='Введите возраст')])
    about = TextAreaField('О себе')
    password = PasswordField('Введите ваш пароль', validators=[DataRequired(message='Введите пароль')])
    submit = SubmitField('Сохранить')
