# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_login import current_user
from flask_restful import abort, Resource
from data.dialogues import Dialogue
from data import db_session
from flask_restful import reqparse
from data.messages import Message

# Парсер аргументов
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('text', required=True)
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('dialogue_id', type=int, required=True)


def abort_if_message_not_found(message_id):
    """Функция проверки существования сообщения.
                Ошибка, если сообщение не найдено."""
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Сообщение {message_id} не найдено")


def abort_if_dialogue_not_found(dialogue_id):
    """Функция проверки существования диалога.
                Ошибка, если диалог не найден."""
    session = db_session.create_session()
    dialogue = session.query(Dialogue).get(dialogue_id)
    if not dialogue:
        abort(404, message=f"Диалог {dialogue_id} не найден")


def abort_if_user_not_found(user_id):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь не найден."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Пользователь {user_id} не найден")


class MessagesResource(Resource):
    """Ресурс Сообщения"""

    def get(self, message_id):
        """Получить одно сообщение"""

        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        return jsonify({'message': message.to_dict(
            only=['id', 'text', 'user_id', 'dialogue_id'])})

    def delete(self, message_id):
        """Удалить сообщение"""

        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    """Ресурс Сообщений"""

    def get(self):
        """Получить все сообщения"""

        session = db_session.create_session()
        messages = session.query(Message).all()
        return jsonify({'messages': [item.to_dict(
            only=['id', 'text', 'user_id', 'dialogue_id']) for item in messages]})

    def post(self):
        """Добавить новое сообщение"""

        args = parser.parse_args()
        session = db_session.create_session()
        # noinspection PyArgumentList
        message = Message(
            text=args['text'],
            user_id=args['user_id'],
            dialogue_id=args['dialogue_id'],
        )
        abort_if_user_not_found(args['user_id'])
        user = session.query(User).get(args['user_id'])
        user.messages.append(message)
        session.merge(user)
        abort_if_dialogue_not_found(args['dialogue_id'])
        dialogue = session.query(Dialogue).get(args['dialogue_id'])
        dialogue.messages.append(message)
        session.merge(dialogue)
        session.add(message)
        session.commit()
        return jsonify({'success': 'OK'})
