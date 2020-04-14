"""ГЛАВНЫЙ ФАЙЛ ПРОЕКТА. СВЯЗЫВАЕТ ВСЕ ОСТАЛЬНЫЕ ФАЙЛЫ ВОЕДИНО."""

# Импорты необходимых библиотек, классов и функций
import os
import requests
from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_ngrok import run_with_ngrok
from flask_restful import Api, abort
from werkzeug.utils import redirect

from data.dialogues import Dialogue
from forms.dialogue_form import DialogueForm
from forms.edit_profile_form import EditProfileForm
from forms.login_form import LoginForm
from data import db_session
from forms.message_form import MessageForm
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
PORT = None


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации."""
    session = db_session.create_session()
    return session.query(User).get(user_id)


@login_required
def get_dialogues():
    """Функция для получения диалогов пользователя."""
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    return [dialogue for dialogue in user.dialogues if str(user.id) in dialogue.members.split(', ')]


@login_required
def get_messages(dialogue_id):
    """Функция для получения сообщений диалога."""
    session = db_session.create_session()
    messages = session.query(Dialogue).get(dialogue_id).messages
    return messages


@login_required
def get_users(dialogue_id):
    """Функция для получения участников диалога."""
    session = db_session.create_session()
    users = session.query(Dialogue).get(dialogue_id).users
    return users


def main():
    """Главная функция. Устанавливает соединение с базой данных.
    Подсоединяет ресурсы. Запускает приложение."""
    global PORT
    db_session.global_init('db/data.sqlite')

    api.add_resource(UsersResource, '/api_users/<int:user_id>')
    api.add_resource(UsersListResource, '/api_users')
    api.add_resource(DialoguesResource, '/api_dialogues/<int:dialogue_id>')
    api.add_resource(DialoguesListResource, '/api_dialogues')
    api.add_resource(MessagesResource, '/api_messages/<int:message_id>')
    api.add_resource(MessagesListResource, '/api_messages')
    api.add_resource(NewsResource, '/api_news/<int:news_id>')
    api.add_resource(NewsListResource, '/api_news')

    PORT = int(os.environ.get("PORT", 5000))
    host = '127.0.0.1'
    app.run()


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
        res = requests.post(f'http://localhost:{PORT}/api_users', json={
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
        res = requests.post(f'http://localhost:{PORT}/api_news', json={
            'content': form.content.data,
            'is_private': form.is_private.data,
            'user_id': current_user.id
        }).json()
        if 'message' in res:
            return render_template('profile.html', title=f'{current_user.name} {current_user.surname}', form=form,
                                   message=res['message'], news=current_user.news)
        return redirect('/profile')
    return render_template('profile.html', title=f'{current_user.name} {current_user.surname}', form=form,
                           news=current_user.news)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Страница редактирования профиля пользователя."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            res = requests.put(f'http://localhost:{PORT}/api_users/{current_user.id}', json={
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


@app.route('/dialogues')
@login_required
def dialogues():
    """Страница пользователя с диалогами."""
    users = {}
    dialogues = get_dialogues()
    for dialogue in dialogues:
        users[dialogue.id] = get_users(dialogue.id)
    return render_template('dialogues.html', title='Диалоги', dialogues=dialogues, users=users)


@app.route('/new_dialogue', methods=['GET', 'POST'])
@login_required
def new_dialogue():
    """Страница для создания нового диалога."""
    form = DialogueForm()
    users = requests.get(f'http://localhost:{PORT}/api_users').json()['users']
    form.members.choices = [(user['id'], f'{user["name"]} {user["surname"]}') for user
                            in users if user['login'] != current_user.login]
    users = {}
    dialogues = get_dialogues()
    for dialogue in dialogues:
        users[dialogue.id] = get_users(dialogue.id)
    if form.validate_on_submit():
        if len(form.members.data) == 1:
            form.name.data = ''
        elif not form.name.data:
            return render_template('/new_dialogue.html', title='Новый диалог', form=form,
                                   message='Введите название беседы', dialogues=dialogues,
                                   users=users)
        res = requests.post(f'http://localhost:{PORT}/api_dialogues', json={
            'name': form.name.data,
            'members': form.members.data + [current_user.id]
        }).json()
        if 'success' in res:
            return redirect('/dialogues')
        return render_template('/new_dialogue.html', title='Новый диалог', form=form,
                               message=res['message'], dialogues=dialogues,
                               users=users)
    return render_template('new_dialogue.html', title='Новый диалог', form=form,
                           dialogues=dialogues, users=users)


@app.route('/dialogue/<int:dialogue_id>', methods=['GET', 'POST'])
@login_required
def get_dialogue(dialogue_id):
    """Страница для получения сообщений диалога"""
    session = db_session.create_session()
    dialogue = session.query(Dialogue).get(dialogue_id)
    if not dialogue:
        abort(505)
    users = {}
    dialogues = get_dialogues()
    for dialogue in dialogues:
        users[dialogue.id] = get_users(dialogue.id)
    dialogue_messages = get_messages(dialogue.id)
    dialogue_users = get_users(dialogue.id)
    form = MessageForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api_messages', json={
            'text': form.text.data,
            'user_id': current_user.id,
            'dialogue_id': dialogue.id
        }).json()
        if 'success' in res:
            return redirect(f'/dialogue/{dialogue.id}')
        abort(500)
    return render_template('dialogue.html', title='Диалоги', dialogue_messages=dialogue_messages,
                           dialogue_users=dialogue_users, users=users,
                           dialogue=dialogue, form=form, dialogues=dialogues)


@app.route('/get_messages', methods=['GET', 'POST'])
def update_messages():
    dialogue_id = request.args.get('dialogue_id')
    messages = get_messages(int(dialogue_id))
    res = {
        'messages': None
    }
    users = get_users(dialogue_id)
    html = ''
    for message in messages:
        user = [user for user in users if user.id == message.user_id][0]
        if user.login == current_user.login:
            html += f"""<div class="row" style="margin: 5px 5px 5px 0px;">
                            <div class="col-6"></div>
                            <div class="col-6 rounded" style="background-color: #EDEDED">
                                <div style="width: 100%;">
                                    <strong>{user.name}{user.surname}</strong>
                                    <small>{str(message.send_date)[:16]}</small>
                                </div>
                                <div>
                                    {message.text}
                                </div>
                            </div>
                        </div>\n"""
        else:
            html += f"""<div class="row" style="margin: 5px 5px 5px 0px;">
                            <div class="col-6 rounded" style="background-color: #EDEDED">
                                <div style="width: 100%;">
                                    <strong>{user.name}{user.surname}</strong>
                                    <small>{str(message.send_date)[:16]}</small>
                                </div>
                                <div>
                                    {message.text}
                                </div>
                            </div>
                            <div class="col-6"></div>
                        </div>\n"""
    res['messages'] = html
    return jsonify(res)


@app.route('/delete_dialogue/<int:dialogue_id>')
@login_required
def delete_dialogue(dialogue_id):
    """Страница для удаления диалога."""
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    for dialogue in user.dialogues:
        if dialogue.id == dialogue_id:
            true_dialogue = session.query(Dialogue).get(dialogue_id)
            true_dialogue.members = ', '.join([member for member in
                                               true_dialogue.members.split(', ')
                                               if int(member) != user.id])
            if true_dialogue.members == '':
                for message in true_dialogue.messages:
                    session.delete(message)
                session.delete(dialogue)
                session.commit()
                break
            session.merge(true_dialogue)
            session.commit()
            break
    return redirect('/dialogues')


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


if __name__ == '__main__':
    main()
