"""ГЛАВНЫЙ ФАЙЛ ПРОЕКТА. СВЯЗЫВАЕТ ВСЕ ОСТАЛЬНЫЕ ФАЙЛЫ ВОЕДИНО."""

# Импорты необходимых библиотек, классов и функций
import os
import requests
from flask import Flask, render_template
from flask_login import LoginManager, login_user, current_user
from flask_restful import Api
from werkzeug.utils import redirect
from forms.loginform import LoginForm
from data.db_session import create_session, global_init
from resources.news_resource import NewsResource, NewsListResource
from data.users import User
from resources.users_resource import UsersListResource, UsersResource
from resources.dialogues_resource import DialoguesResource, DialoguesListResource
from resources.messages_resource import MessagesResource, MessagesListResource

# Создание приложения, API и менеджера авторизации
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации"""
    session = create_session()
    return session.query(User).get(user_id)


def main():
    """Главная функция. Устанавливает соединение с базой данных.
    Подсоединяет ресурсы. Запускает приложение"""
    global_init('db/data.sqlite')

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
    return render_template('error.html', error=str(error).split(': ')), 404


@app.errorhandler(500)
def bad_request(error):
    """Отлавливает ошибку 500. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 500


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/news')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/logout')
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/news')
        return render_template('login.html', title='Авторизация',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
