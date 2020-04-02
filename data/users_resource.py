# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.users import User
from flask_restful import reqparse

# Парсер аргументов
parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', type=int, required=True)
parser.add_argument('about', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь не найден."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_user_already_exists(user_login):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь уже существует."""
    session = db_session.create_session()
    user = session.query(User).filter(User.login == user_login).first()
    if user:
        abort(404, message=f"User with login='{user_login}' already exists")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in users]})

    def post(self):
        args = parser.parse_args()
        abort_if_user_already_exists(args['login'])
        session = db_session.create_session()
        # noinspection PyArgumentList
        user = User(
            login=args['login'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            about=args['about'],
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
