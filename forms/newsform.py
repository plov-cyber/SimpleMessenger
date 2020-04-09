from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    content = TextAreaField('Какие новости?', validators=[DataRequired(message='Обязательное поле')])
    is_private = BooleanField('Приватная')
    submit = SubmitField('Опубликовать')
