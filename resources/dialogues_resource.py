# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_restful import abort, Resource
from data.users import User
from data import db_session
from flask_restful import reqparse
from data.dialogues import Dialogue

# Парсер аргументов
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('members', required=True, action='append', type=int)


def abort_if_dialogue_not_found(dialogue_id):
    """Функция проверки существования диалога.
            Ошибка, если диалог не найден."""
    session = db_session.create_session()
    dialogue = session.query(Dialogue).get(dialogue_id)
    if not dialogue:
        abort(404, message="Диалог {} не найден".format(dialogue_id))


def check_if_dialogue_already_exists(name, members):
    """Функция проверки существования диалога."""
    session = db_session.create_session()
    dialogues = session.query(Dialogue).filter(Dialogue.name == name).all()
    for dialogue in dialogues:
        if sorted(members) == sorted([user.id for user in dialogue.users]):
            return True
    return False


def abort_if_user_not_found(user_id):
    """Функция проверки существования пользователя.
        Ошибка, если пользователь не найден."""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message="Пользователь {} не найден".format(user_id))


class DialoguesResource(Resource):
    """Ресурс Диалога"""

    def get(self, dialogue_id):
        """Получить один диалог"""

        abort_if_dialogue_not_found(dialogue_id)
        session = db_session.create_session()
        dialogue = session.query(Dialogue).get(dialogue_id)
        return jsonify({'dialogue': dialogue.to_dict(only=['id', 'name', 'members'])})

    def delete(self, dialogue_id):
        """Удалить диалог"""

        abort_if_dialogue_not_found(dialogue_id)
        session = db_session.create_session()
        dialogue = session.query(Dialogue).get(dialogue_id)
        session.delete(dialogue)
        session.commit()
        return jsonify({'success': 'OK'})


class DialoguesListResource(Resource):
    """Ресурс Диалогов"""

    def get(self):
        """Получить все диалоги"""

        session = db_session.create_session()
        dialogues = session.query(Dialogue).all()
        return jsonify({'dialogues': [item.to_dict(only=['id', 'name', 'members']) for item in dialogues]})

    def post(self):
        """Добавить новый диалог"""

        args = parser.parse_args()
        session = db_session.create_session()
        if check_if_dialogue_already_exists(args['name'], args['members']):
            dialogues = session.query(Dialogue).filter(Dialogue.name == args['name']).all()
            for d in dialogues:
                if sorted([user.id for user in d.users]) == sorted(args['members']):
                    dialogue = d
                    break
            user = [u for u in dialogue.users if str(u.id) not in dialogue.members.split(', ')]
            if not user:
                if len(args['members']) == 2:
                    abort(404, message='Диалог уже существует')
                else:
                    abort(404, message='Беседа уже существует')
            user = user[0]
            dialogue.members += ', ' + str(user.id)
            session.merge(dialogue)
            session.commit()
            return jsonify({'success': 'OK'})
        # noinspection PyArgumentList
        dialogue = Dialogue(
            name=args['name'],
            members=', '.join(list(map(str, args['members'])))
        )
        for user_id in args['members']:
            abort_if_user_not_found(user_id)
            user = session.query(User).get(user_id)
            user.dialogues.append(dialogue)
            session.merge(user)
        session.add(dialogue)
        session.commit()
        return jsonify({'success': 'OK'})
