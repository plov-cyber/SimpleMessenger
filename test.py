"""ФАЙЛ ДЛЯ ТЕСТИРОВАНИЯ РАБОТЫ БАЗЫ ДАННЫХ."""

# Импорты необходимых библиотек, классов и функций
from requests import get, post, delete

# Корректные запросы
# Создание пользователя
print(post('http://127.0.0.1:5000/sm/users', json={
    'login': '1',
    'name': '1',
    'surname': '1',
    'age': '1',
    'about': '1',
    'password': '1'
}).json())
print(post('http://127.0.0.1:5000/sm/users', json={
    'login': '2',
    'name': '2',
    'surname': '2',
    'age': '2',
    'about': '2',
    'password': '2'
}).json())
print(get('http://127.0.0.1:5000/sm/users').json())
print(get('http://127.0.0.1:5000/sm/users/1').json())
print(get('http://127.0.0.1:5000/sm/users/2').json())
# Создание диалога
print(post('http://127.0.0.1:5000/sm/dialogues', json={
    'name': 'Test dialog',
    'members': [1, 2]
}).json())
print(get('http://127.0.0.1:5000/sm/dialogues').json())
print(get('http://127.0.0.1:5000/sm/dialogues/1').json())
