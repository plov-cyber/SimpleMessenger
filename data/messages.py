# Импорты необходимых библиотек, классов и функций
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    """Класс Сообщения"""
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    dialogue_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('dialogues.id'), nullable=False)
    user = orm.relation('User')
    dialogue = orm.relation('Dialogue')
