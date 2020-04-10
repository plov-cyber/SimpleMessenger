# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    """Класс формы для редактирования профиля"""
    surname = StringField('Фамилия', validators=[DataRequired(message='Обязательное поле')])
    name = StringField('Имя', validators=[DataRequired(message='Обязательное поле')])
    age = IntegerField('Возраст', validators=[DataRequired(message='Обязательное поле')])
    about = TextAreaField('О себе')
    password = PasswordField('Введите ваш пароль', validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Сохранить')
