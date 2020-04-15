# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс Пользователя"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    dialogues = orm.relation('Dialogue', secondary='user_to_dialogue', backref='users')
    messages = orm.relation('Message', back_populates='user')
    news = orm.relation("News", back_populates='user')

    def set_password(self, password):
        """Функция установки пароля"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Функция проверки пароля"""
        return check_password_hash(self.hashed_password, password)
