import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    dialogue_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('dialogues.id'))
    user = orm.relation('User')
    dialogue = orm.relation('Dialogue')
