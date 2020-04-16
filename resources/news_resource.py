# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask import jsonify
from flask_login import current_user
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.news import News

# Парсер аргументов
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('is_private', type=bool, required=True)
parser.add_argument('user_id', type=int, required=True)


def abort_if_news_not_found(news_id):
    """Функция проверки существования новости.
            Ошибка, если новость не найдена."""
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message="Новость {} не найдена".format(news_id))


class NewsResource(Resource):
    """Ресурс Новости"""

    def get(self, news_id):
        """Получить одну новость"""

        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(only=['content', 'is_private', 'user_id'])})

    def delete(self, news_id):
        """Удалить новость"""

        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, news_id):
        """Редактировать новость"""

        abort_if_news_not_found(news_id)
        args = parser.parse_args()
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        news.content = args['content']
        news.is_private = args['is_private']
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    """Ресурс Новостей"""

    def get(self):
        """Получить все новости"""

        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({'news': [item.to_dict(only=['content', 'is_private', 'user_id']) for item in news]})

    def post(self):
        """Добавить новую новость"""

        args = parser.parse_args()
        session = db_session.create_session()
        # noinspection PyArgumentList
        news = News(
            content=args['content'],
            user_id=args['user_id'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})
