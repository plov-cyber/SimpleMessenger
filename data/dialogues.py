# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

# Промежуточная таблица связи пользователей и диалогов
user_to_dialogue = sqlalchemy.Table('user_to_dialogue', SqlAlchemyBase.metadata,
                                    sqlalchemy.Column('user', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('users.id')),
                                    sqlalchemy.Column('dialogue', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('dialogues.id')))


class Dialogue(SqlAlchemyBase, SerializerMixin):
    """Класс Диалога"""
    __tablename__ = 'dialogues'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    messages = orm.relation('Message', back_populates='dialogue')
