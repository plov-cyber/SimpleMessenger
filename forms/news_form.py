# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    """Класс формы для создания и редактирования новости"""
    content = TextAreaField('Какие новости?', validators=[DataRequired(message='Вы не написали никаких новостей')])
    is_private = BooleanField('Приватная')
    submit = SubmitField('Опубликовать')
