import os

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_restful import Api
from flask import make_response
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/data.sqlite')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
