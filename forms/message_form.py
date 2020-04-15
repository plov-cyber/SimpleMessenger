# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    """Класс формы для отправки сообщений"""
    text = TextAreaField('Введите сообщение', validators=[DataRequired()])
    submit = SubmitField('▲')
