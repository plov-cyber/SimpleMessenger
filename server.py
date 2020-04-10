"""ГЛАВНЫЙ ФАЙЛ ПРОЕКТА. СВЯЗЫВАЕТ ВСЕ ОСТАЛЬНЫЕ ФАЙЛЫ ВОЕДИНО."""

# Импорты необходимых библиотек, классов и функций
import os
import requests
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_ngrok import run_with_ngrok
from flask_restful import Api
from werkzeug.utils import redirect

from forms.edit_profile_form import EditProfileForm
from forms.login_form import LoginForm
from data import db_session
from forms.news_form import NewsForm
from forms.reg_form import RegisterForm
from resources.news_resource import NewsResource, NewsListResource
from data.users import User
from resources.users_resource import UsersListResource, UsersResource
from resources.dialogues_resource import DialoguesResource, DialoguesListResource
from resources.messages_resource import MessagesResource, MessagesListResource

# Создание приложения, API и менеджера авторизации
app = Flask(__name__)
# run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации."""
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    """Главная функция. Устанавливает соединение с базой данных.
    Подсоединяет ресурсы. Запускает приложение."""
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
    """Отлавливает ошибку 404 Not Found. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 404


@app.errorhandler(500)
def bad_request(error):
    """Отлавливает ошибку 500 Bad Request. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 500


@app.errorhandler(401)
def unauthorized(error):
    """Отлавливает ошибку 401 Unauthorized. Перенаправляет пользователя на страницу для входа."""
    return redirect('/login')


@app.route('/')
def index():
    """Перенаправляет пользователя на страницу с новостями, либо на страницу входа."""
    return redirect('/news')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации пользователя."""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        res = requests.post('http://127.0.0.1:5000/users', json={
            'login': form.login.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'age': form.age.data,
            'about': '',
            'password': form.password.data
        }).json()
        if 'message' in res:
            return render_template('register.html', title='Регистрация', form=form,
                                   message=res['message'])
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в аккаунт пользователя."""
    if current_user.is_authenticated:
        return redirect('/logout')
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/news')
        return render_template('login.html', title='Авторизация',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    """Страница для выхода пользователя."""
    logout_user()
    return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Страница профиля пользователя."""
    form = NewsForm()
    if form.validate_on_submit():
        res = requests.post('http://127.0.0.1:5000/news', json={
            'content': form.content.data,
            'is_private': form.is_private.data,
            'user_id': current_user.id
        }).json()
        if 'message' in res:
            return render_template('profile.html', title=f'{current_user.name} {current_user.surname}', form=form,
                                   message=res['message'])
        return redirect('/profile')
    return render_template('profile.html', title=f'{current_user.name} {current_user.surname}', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Страница редактирования профиля пользователя."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            res = requests.put(f'http://127.0.0.1:5000/users/{current_user.id}', json={
                'login': current_user.login,
                'name': form.name.data,
                'surname': form.surname.data,
                'age': form.age.data,
                'about': form.about.data if form.about.data else '',
                'password': form.password.data
            }).json()
            if 'success' in res:
                return render_template('profile_edit.html', title='Редактирование профиля',
                                       message='Изменения успешно сохранены', form=form)
            return render_template('profile_edit.html', title='Редактирование профиля',
                                   error=res['message'], form=form)
        return render_template('profile_edit.html', title='Редактирование профиля',
                               error='Неправильный пароль', form=form)
    form.surname.data = current_user.surname
    form.name.data = current_user.name
    form.age.data = current_user.age
    form.about.data = current_user.about
    return render_template('profile_edit.html', title='Редактирование профиля', form=form)


@app.route('/settings')
@login_required
def settings():
    """Страница настроек пользователя."""
    return render_template('base.html', title='Настройки')


@app.route('/news')
@login_required
def news():
    """Страница с новостями других пользователей."""
    return render_template('news.html', title='Новости')


@app.route('/messages')
@login_required
def messages():
    """Страница пользователя с диалогами."""
    return render_template('base.html', title='Диалоги')


if __name__ == '__main__':
    main()
