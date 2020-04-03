"""ГЛАВНЫЙ ФАЙЛ ПРОЕКТА. СВЯЗЫВАЕТ ВСЕ ОСТАЛЬНЫЕ ФАЙЛЫ ВОЕДИНО."""

# Импорты необходимых библиотек, классов и функций
import os

import requests
from flask import Flask, render_template
from flask_login import LoginManager, login_user
from flask_restful import Api
from data import db_session
from data.news_resource import NewsResource, NewsListResource
from data.users import User
from data.users_resource import UsersListResource, UsersResource
from data.dialogues_resource import DialoguesResource, DialoguesListResource
from data.messages_resource import MessagesResource, MessagesListResource

# Создание приложения, API и менеджера авторизации
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации"""
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    """Главная функция. Устанавливает соединение с базой данных.
    Подсоединяет ресурсы. Запускает приложение"""
    db_session.global_init('db/data.sqlite')

    api.add_resource(UsersResource, '/users/<int:user_id>')
    api.add_resource(UsersListResource, '/users')
    api.add_resource(DialoguesResource, '/dialogues/<int:dialogue_id>')
    api.add_resource(DialoguesListResource, '/dialogues')
    api.add_resource(MessagesResource, '/messages/<int:message_id>')
    api.add_resource(MessagesListResource, '/messages')
    api.add_resource(NewsResource, '/news/<int:news_id>')
    api.add_resource(NewsListResource, '/news')

    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)


@app.errorhandler(404)
def not_found(error):
    """Отлавливает ошибку 404. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': '))


if __name__ == '__main__':
    main()
