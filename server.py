# coding=utf-8
"""ГЛАВНЫЙ ФАЙЛ ПРОЕКТА. СВЯЗЫВАЕТ ВСЕ ОСТАЛЬНЫЕ ФАЙЛЫ ВОЕДИНО."""

# Импорты необходимых библиотек, классов и функций
import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_ngrok import run_with_ngrok
from flask_restful import Api, abort
from werkzeug.utils import redirect

from data.dialogues import Dialogue
from data.news import News
from forms.change_pwd_form import NewPasswordForm
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
    return [dialogue for dialogue in user.dialogues if
            str(user.id) in dialogue.members.split(', ')]


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


@login_required
def get_news():
    """Функция для получения всех новостей."""
    session = db_session.create_session()
    news = session.query(News).all()
    return news


@login_required
def get_user(user_id):
    """Функция для получения пользователя."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(500)
    return user


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

    PORT = int(os.environ.get("PORT", 80))
    # '0.0.0.0', port=PORT
    app.run('0.0.0.0', port=PORT)


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
        res = requests.post('http://localhost:{}/api_users'.format(PORT), json={
            'login': form.login.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'age': form.age.data,
            'about': '',
            'friends': '',
            'friend_requests': '',
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

            next_url = request.args.get('next')
            return redirect(next_url or '/news')
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


@app.route('/my_profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    """Страница профиля пользователя."""
    form = NewsForm()
    if form.validate_on_submit():
        res = requests.post('http://localhost:{}/api_news'.format(PORT), json={
            'content': form.content.data,
            'is_private': form.is_private.data,
            'user_id': current_user.id
        }).json()
        if 'message' in res:
            return render_template('my_profile.html', form=form,
                                   title='{} {}'.format(current_user.name, current_user.surname),
                                   message=res['message'], news=current_user.news)
        return redirect('/profile')
    return render_template('my_profile.html', title='{} {}'.format(current_user.name, current_user.surname),
                           form=form, news=current_user.news)


@app.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    """Страница профиля другого пользователя."""
    if user_id == current_user.id:
        return redirect('/my_profile')
    user = get_user(user_id)
    news = []
    for article in user.news:
        art = requests.get('http://localhost:{}/api_news/{}'.format(PORT, article.id)).json()
        if 'news' not in art:
            abort(500)
        news.append(art['news'])
    current_user_friends = list(map(int, current_user.friends.split(', '))) if current_user.friends else []
    current_user_friend_requests = list(
        map(int, current_user.friend_requests.split(', '))) if current_user.friend_requests else []
    user_friend_requests = list(map(int, user.friend_requests.split(', '))) if user.friend_requests else []
    return render_template('profile.html', title='{} {}'.format(user.name, user.surname), news=news,
                           user=user, current_user_friend_requests=current_user_friend_requests,
                           current_user_friends=current_user_friends, user_friend_requests=user_friend_requests)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Страница редактирования профиля пользователя."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            res = requests.put('http://localhost:{}/api_users/{}'.format(PORT, current_user.id), json={
                'login': current_user.login,
                'name': form.name.data,
                'surname': form.surname.data,
                'age': form.age.data,
                'about': form.about.data if form.about.data else '',
                'friends': current_user.friends,
                'friend_requests': current_user.friend_requests,
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


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Страница настроек пользователя."""
    form = NewPasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            if form.old_password.data != form.new_password.data:
                res = requests.put('http://localhost:{}/api_users/{}'.format(PORT, current_user.id), json={
                    'login': current_user.login,
                    'name': current_user.name,
                    'surname': current_user.surname,
                    'age': current_user.age,
                    'about': current_user.about,
                    'friends': current_user.friends,
                    'password': form.new_password.data
                }).json()
                if 'success' in res:
                    return render_template('settings.html', title='Настройки', form=form,
                                           message='Пароль успешно изменён')
                return render_template('settings.html', title='Настройки', form=form,
                                       error=res['message'])
            return render_template('settings.html', title='Настройки', form=form,
                                   error='Старый и новый пароли совпадают!')
        return render_template('settings.html', title='Настройки', form=form,
                               error='Неверный пароль')
    return render_template('settings.html', title='Настройки', form=form)


@app.route('/delete_profile/<int:user_id>')
@login_required
def delete_profile(user_id):
    """Функция для удаления профиля пользователя."""
    res = requests.delete('http://localhost:{}/api_users/{}'.format(PORT, user_id)).json()
    if 'success' in res:
        return redirect('/logout')
    abort(500)


@app.route('/dialogues')
@login_required
def my_dialogues():
    """Страница пользователя с диалогами."""
    users = {}
    all_dialogues = get_dialogues()
    dialogues = []
    for dialogue in all_dialogues:
        if len(dialogue.members.split(', ')) == 2:
            user_id = [i for i in dialogue.members.split(', ') if i != str(current_user.id)][0]
            if user_id in current_user.friends.split(', '):
                dialogues.append(dialogue)
        else:
            dialogues.append(dialogue)
    for dialogue in dialogues:
        users[dialogue.id] = get_users(dialogue.id)
    return render_template('dialogues.html', title='Диалоги', dialogues=dialogues, users=users)


@app.route('/new_dialogue', methods=['GET', 'POST'])
@login_required
def new_dialogue():
    """Страница для создания нового диалога."""
    form = DialogueForm()
    users = requests.get('http://localhost:{}/api_users'.format(PORT)).json()['users']
    form.members.choices = [(user['id'], '{} {}'.format(user['name'], user['surname'])) for user
                            in users if user['login'] != current_user.login and
                            str(user['id']) in current_user.friends.split(', ')]
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
        res = requests.post('http://localhost:{}/api_dialogues'.format(PORT), json={
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
        res = requests.post('http://localhost:{}/api_messages'.format(PORT), json={
            'text': form.text.data,
            'user_id': current_user.id,
            'dialogue_id': dialogue.id
        }).json()
        if 'success' in res:
            return redirect('/dialogue/{}'.format(dialogue.id))
        abort(500)
    return render_template('dialogue.html', title='Диалоги', dialogue_messages=dialogue_messages,
                           dialogue_users=dialogue_users, users=users,
                           dialogue=dialogue, form=form, dialogues=dialogues)


@app.route('/get_messages', methods=['GET', 'POST'])
@login_required
def update_messages():
    """Функиця для обновления сообшений в диалоге."""
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
            html += """<div class="row justify-content-end" style="margin: 5px 5px 5px 0px;">
                            <div class="col-md-auto rounded" style="background-color: #EDEDED; text-align: right;">
                                <div style="width: 100%;">
                                    <small>{}</small>
                                    <strong>{} {}</strong>
                                </div>
                                <div>
                                    {}
                                </div>
                            </div>
                        </div>\n""".format(str(message.send_date)[:16], user.name, user.surname, message.text)
        else:
            html += """<div class="row justify-content-start" style="margin: 5px 0px 5px 5px;">
                            <div class="col-md-auto rounded" style="background-color: #EDEDED; text-align: left;">
                                <div style="width: 100%;">
                                    <strong>{} {}</strong>
                                    <small>{}</small>
                                </div>
                                <div>
                                    {}
                                </div>
                            </div>
                        </div>\n""".format(user.name, user.surname, str(message.send_date)[:16], message.text)
        if message == messages[-1]:
            html += """<div id="bottom"></div>\n"""
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


@app.route('/news', methods=['GET', 'POST'])
@login_required
def all_news():
    """Страница с новостями других пользователей."""
    news = requests.get('http://localhost:{}/api_news'.format(PORT)).json()
    if 'news' not in news:
        abort(500)
    news = news['news']
    users = {}
    for article in news:
        user = requests.get('http://localhost:{}/api_users/{}'.format(PORT, article['user_id'])).json()
        if 'user' not in user:
            abort(500)
        user = user['user']
        users[article['id']] = '{} {}'.format(user['name'], user['surname'])
    form = NewsForm()
    if form.validate_on_submit():
        res = requests.post('http://localhost:{}/api_news'.format(PORT), json={
            'content': form.content.data,
            'is_private': form.is_private.data,
            'user_id': current_user.id
        }).json()
        if 'message' in res:
            return render_template('news.html', title='Новости',
                                   form=form, message=res['message'],
                                   news=news, users=users)
        return redirect('/news')
    return render_template('news.html', title='Новости', news=news, users=users, form=form)


@app.route('/delete_news/<int:news_id>')
@login_required
def delete_news(news_id):
    """Функция для удаления новости пользователя."""
    res = requests.delete('http://localhost:{}/api_news/{}'.format(PORT, news_id)).json()
    if 'success' in res:
        return redirect(request.referrer)
    abort(500)


@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    """Страница для редактирования новости пользователя."""
    form = NewsForm()
    news = requests.get('http://localhost:{}/api_news/{}'.format(PORT, news_id)).json()
    if 'news' not in news:
        abort(500)
    news = news['news']
    if form.validate_on_submit():
        res = requests.put('http://localhost:{}/api_news/{}'.format(PORT, news_id), json={
            'content': form.content.data,
            'is_private': form.is_private.data,
            'user_id': current_user.id
        }).json()
        if 'success' in res:
            return render_template('edit_news.html', title='Редактирование новости', form=form,
                                   message='Изменения успешно сохранены')
        return render_template('edit_news.html', title='Редактирование новости', form=form,
                               error=res['message'])
    form.content.data = news['content']
    form.is_private.data = news['is_private']
    return render_template('edit_news.html', title='Редактирование новости', form=form)


@app.route('/get_news', methods=['GET', 'POST'])
def update_news():
    """Функция для обновления новостей в ленте."""
    news = get_news()
    res = {
        'news': None
    }
    html = ''
    for article in news[::-1]:
        if not article.is_private:
            html += """<div class="container-fluid shadow-sm rounded" 
            style="background-color: #F0F0F0; padding-bottom: 10px;">\n"""
            html += """<div class="row">
                           <div class="col-10">
                               <h3>{}</h3>
                               <small>{}</small>
                           </div>
                       </div>

                       <div class="row">
                           <div class="col-12">
                               <h5>{}</h5>
                           </div>
                       </div>\n""".format('{} {}'.format(article.user.name, article.user.surname),
                                          str(article.created_date)[:16], article.content)
            if article.user_id == current_user.id:
                html += """<div class="row">
                               <div class="col-5">
                                   <a href="/edit_news/{{ article.id }}" class="btn btn-secondary">
                                       Редактировать
                                   </a>
                                   <a href="/delete_news/{{ article.id }}" class="btn btn-danger">
                                       Удалить
                                   </a>
                               </div>
                           </div>\n""".format(article.id, article.id)
            html += """</div>
                       <br>\n"""
    res['news'] = html
    return jsonify(res)


@app.route('/friends')
@login_required
def my_friends():
    """Страница с друзьями пользователя."""
    friends = []
    if current_user.friends:
        for user_id in list(map(int, current_user.friends.split(', '))):
            friend = requests.get('http://localhost:{}/api_users/{}'.format(PORT, user_id)).json()
            if 'user' not in friend:
                abort(500)
            friends.append(friend['user'])
    return render_template('friends.html', title='Друзья', friends=friends)


@app.route('/add_request/<int:user_id>')
@login_required
def add_request(user_id):
    """Функция для добавления заявки в друзья."""
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if user.friend_requests:
        user.friend_requests += ', ' + str(user_id)
    else:
        user.friend_requests = str(user_id)
    session.merge(user)
    session.commit()
    return redirect('/profile/{}'.format(user_id))


@app.route('/delete_request/<int:user_id>/<int:type>')
@login_required
def delete_request(user_id, type):
    """Функция для удаления заявки в друзья."""
    session = db_session.create_session()
    user = None
    if type == 1:
        user = session.query(User).get(current_user.id)
        user.friend_requests = ', '.join([i for i in user.friend_requests.split(', ') if i != str(user_id)])
    elif type == 2:
        user = session.query(User).get(user_id)
        user.friend_requests = ', '.join([i for i in user.friend_requests.split(', ') if i != str(current_user.id)])
    else:
        abort(500)
    session.merge(user)
    session.commit()
    return redirect('/profile/{}'.format(user_id))


@app.route('/add_friend/<int:user_id>')
@login_required
def add_friend(user_id):
    """Функция для добавления пользователя в друзья."""
    delete_request(user_id, 2)
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if user.friends:
        user.friends += ', ' + str(user_id)
    else:
        user.friends = str(user_id)
    session.merge(user)
    session.commit()
    user = session.query(User).get(user_id)
    if user.friends:
        user.friends += ', ' + str(current_user.id)
    else:
        user.friends = str(current_user.id)
    session.merge(user)
    session.commit()
    return redirect(request.referrer)


@app.route('/delete_friend/<int:user_id>')
@login_required
def delete_friend(user_id):
    """Функция для удаления пользователя из друзей."""
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    user.friends = ', '.join([i for i in user.friends.split(', ') if i != str(user_id)])
    session.merge(user)
    session.commit()
    user = session.query(User).get(user_id)
    user.friends = ', '.join([i for i in user.friends.split(', ') if i != str(current_user.id)])
    session.merge(user)
    session.commit()
    return redirect('/profile/{}'.format(user_id))


@app.route('/friend_requests')
@login_required
def friend_requests():
    users = requests.get('http://localhost:{}/api_users'.format(PORT)).json()
    if 'users' not in users:
        abort(500)
    users = [user for user in users['users'] if user['id'] != current_user.id]
    followers = []
    for user in users:
        if user['friend_requests'] and current_user.id in list(map(int, user['friend_requests'].split(', '))):
            followers.append(user)
    return render_template('friend_requests.html', title='Заявки в друзья', followers=followers)


@app.route('/find_friends')
@login_required
def find_friends():
    users = requests.get('http://localhost:{}/api_users'.format(PORT)).json()
    if 'users' not in users:
        abort(500)
    users = [user for user in users['users'] if user['id'] != current_user.id]
    strangers = []
    if current_user.friends:
        for user in users:
            if user['id'] not in list(map(int, current_user.friends.split(', '))):
                strangers.append(user)
    else:
        strangers = users
    current_user_friend_requests = list(
        map(int, current_user.friend_requests.split(', '))) if current_user.friend_requests else []
    user_friend_requests = list(map(int, user.friend_requests.split(', '))) if user.friend_requests else []
    return render_template('find_friends.html', strangers=strangers, title='Найти друзей',
                           current_user_friend_requests=current_user_friend_requests,
                           user_friend_requests=user_friend_requests)


if __name__ == '__main__':
    main()
