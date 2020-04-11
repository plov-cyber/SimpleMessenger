# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class DialogueForm(FlaskForm):
    """Класс формы для создания диалога"""
    name = StringField('Название беседы', validators=[DataRequired(message='Обязательное поле')])
    members = MultiCheckboxField('Собеседники', coerce=int,
                                 validators=[DataRequired(message='Выберите собеседника')])
    submit = SubmitField('Создать')
