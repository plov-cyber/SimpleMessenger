# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.dialogues import Dialogue
from data.users import User
from flask_restful import reqparse

# Парсер аргументов
parser = reqparse.RequestParser()
parser.add_argument('login', type=str, required=True)
parser.add_argument('name', type=str, required=True)
parser.add_argument('surname', type=str, required=True)
parser.add_argument('age', type=int, required=True)
parser.add_argument('about', type=str, required=True)
parser.add_argument('friends', type=str, required=True)
parser.add_argument('friend_requests', type=str, required=True)
parser.add_argument('password', type=str, required=True)


def abort_if_user_not_found(user_id):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь не найден."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message="Пользователь {} не найден".format(user_id))


def abort_if_user_already_exists(user_login):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь уже существует."""
    session = db_session.create_session()
    user = session.query(User).filter(User.login == user_login).first()
    if user:
        abort(404, message="Пользователь с логином: '{}' уже существует".format(user_login))


def abort_if_age_neg(age):
    """Функция проверки возраста на отрицательность."""
    if age < 0:
        abort(404, message='Возраст не может быть отрицательным')


class UsersResource(Resource):
    """Ресурс Пользователя"""

    def get(self, user_id):
        """Получить одного пользователя"""

        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=['id', 'login', 'name', 'surname', 'age', 'about', 'friends', 'friend_requests'])})

    def delete(self, user_id):
        """Удалить пользователя"""

        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        for news in user.news:
            session.delete(news)
            session.commit()
        for message in user.messages:
            session.delete(message)
            session.commit()
        for dialogue in user.dialogues:
            d = session.query(Dialogue).get(dialogue.id)
            d.members = ', '.join([i for i in d.members.split(', ') if i != str(user.id)])
            if not d.members:
                session.delete(d)
            else:
                session.merge(d)
            session.commit()
        if user.friends:
            for user_id in list(map(int, user.friends.split(', '))):
                abort_if_user_not_found(user_id)
                friend = session.query(User).get(user_id)
                friend.friends = ', '.join([i for i in friend.friends.split(', ') if i != str(user.id)])
                session.merge(friend)
                session.commit()
        if user.friend_requests:
            users = session.query(User).all()
            for person in users:
                if user.id in [int(i) for i in person.friend_requests.split(', ')]:
                    person.friend_requests = ', '.join(
                        [i for i in person.friend_requests.split(', ') if i != str(user.id)])
                    session.merge(person)
                    session.commit()
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        """Изменить данные пользователя"""

        args = parser.parse_args()
        abort_if_user_not_found(user_id)
        abort_if_age_neg(args['age'])
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.name = args['name']
        user.surname = args['surname']
        user.age = args['age']
        user.about = args['about']
        user.friends = args['friends']
        user.friend_requests = args['friend_requests']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Ресурс Пользователей"""

    def get(self):
        """Получить всех пользователей"""

        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [
            item.to_dict(
                only=['id', 'login', 'name', 'surname', 'age', 'about', 'friends', 'friend_requests']) for
            item in users]})

    def post(self):
        """Добавить нового пользователя"""

        args = parser.parse_args()
        abort_if_user_already_exists(args['login'])
        abort_if_age_neg(args['age'])
        session = db_session.create_session()
        # noinspection PyArgumentList
        user = User(
            login=args['login'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            about=args['about'],
            friends=args['friends'],
            friend_requests=args['friend_requests']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
