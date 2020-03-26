from flask import jsonify
from flask_login import current_user
from flask_restful import abort, Resource

from data.dialogues import Dialogue
from data import db_session
from flask_restful import reqparse
from data.messages import Message

parser = reqparse.RequestParser()
parser.add_argument('text', required=True)
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('dialogue_id', type=int, required=True)


def abort_if_message_not_found(message_id):
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Message {message_id} not found")


def abort_if_dialogue_not_found(dialogue_id):
    session = db_session.create_session()
    dialogue = session.query(Dialogue).get(dialogue_id)
    if not dialogue:
        abort(404, message=f"Dialogue {dialogue_id} not found")


class MessagesResource(Resource):
    def get(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        return jsonify({'message': message.to_dict()})

    def delete(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        messages = session.query(Message).all()
        return jsonify({'messages': [item.to_dict() for item in messages]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        # noinspection PyArgumentList
        message = Message(
            text=args['text'],
            user_id=args['user_id'],
            dialogue_id=args['dialogue_id']
        )
        current_user.messages.append(message)
        abort_if_dialogue_not_found(args['dialogue_id'])
        dialogue = session.query(Dialogue).get(args['dialogue_id'])
        dialogue.messages.append(message)
        session.merge(dialogue)
        session.merge(current_user)
        session.add(message)
        session.commit()
        return jsonify({'success': 'OK'})
