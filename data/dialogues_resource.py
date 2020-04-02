# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_login import current_user
from flask_restful import abort, Resource
from data.users import User
from data import db_session
from flask_restful import reqparse
from data.dialogues import Dialogue

# Парсер аргументов
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('members', required=True, action='append')


def abort_if_dialogue_not_found(dialogue_id):
    """Функция проверки существования диалога.
            Ошибка, если диалог не найден."""
    session = db_session.create_session()
    dialogue = session.query(Dialogue).get(dialogue_id)
    if not dialogue:
        abort(404, message=f"Dialogue {dialogue_id} not found")


def abort_if_dialogue_already_exists(name, members):
    """Функция проверки существования диалога.
                Ошибка, если диалог уже существует."""
    session = db_session.create_session()
    dialogue = session.query(Dialogue).filter(Dialogue.name == name).first()
    if dialogue and members == [user.id for user in dialogue.users]:
        abort(404, message=f"Dialogue with name='{name}' and members='{members}' already exists")


def abort_if_user_not_found(user_id):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь не найден."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class DialoguesResource(Resource):
    def get(self, dialogue_id):
        abort_if_dialogue_not_found(dialogue_id)
        session = db_session.create_session()
        dialogue = session.query(Dialogue).get(dialogue_id)
        return jsonify({'dialogue': dialogue.to_dict(only=['id', 'name', 'messages'])})

    def delete(self, dialogue_id):
        abort_if_dialogue_not_found(dialogue_id)
        session = db_session.create_session()
        dialogue = session.query(Dialogue).get(dialogue_id)
        session.delete(dialogue)
        session.commit()
        return jsonify({'success': 'OK'})


class DialoguesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        dialogues = session.query(Dialogue).all()
        return jsonify({'dialogues': [item.to_dict(only=['id', 'name', 'messages']) for item in dialogues]})

    def post(self):
        args = parser.parse_args()
        abort_if_dialogue_already_exists(args['name'], args['members'])
        session = db_session.create_session()
        # noinspection PyArgumentList
        dialogue = Dialogue(
            name=args['name']
        )
        if current_user.is_authenticated:
            current_user.dialogues.append(dialogue)
            session.merge(current_user)
        for user_id in args['members']:
            abort_if_user_not_found(user_id)
            user = session.query(User).get(user_id)
            user.dialogues.append(dialogue)
            session.merge(user)
        session.add(dialogue)
        session.commit()
        return jsonify({'success': 'OK'})
