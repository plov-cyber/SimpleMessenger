"""ФАЙЛ ДЛЯ ТЕСТИРОВАНИЯ РАБОТЫ БАЗЫ ДАННЫХ."""

# Импорты необходимых библиотек, классов и функций
from requests import get, post, delete

# Корректные запросы
# Тестирование пользователя
print(post('http://127.0.0.1:5000/users', json={
    'login': '1',
    'name': '1',
    'surname': '1',
    'age': '1',
    'about': '1',
    'password': '1'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '2',
    'name': '2',
    'surname': '2',
    'age': '2',
    'about': '2',
    'password': '2'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'age': '3',
    'about': '3',
    'password': '3'
}).json())
print(get('http://127.0.0.1:5000/users').json())
print(delete('http://127.0.0.1:5000/users/3').json())
print(get('http://127.0.0.1:5000/users/1').json())
print(get('http://127.0.0.1:5000/users/2').json())
print(get('http://127.0.0.1:5000/users').json())
# Тестирование диалога
print(post('http://127.0.0.1:5000/dialogues', json={
    'name': 'Test dialog 1',
    'members': [1, 2]
}).json())
print(post('http://127.0.0.1:5000/dialogues', json={
    'name': 'Test dialog 2',
    'members': [1, 2]
}).json())
print(get('http://127.0.0.1:5000/dialogues').json())
print(delete('http://127.0.0.1:5000/dialogues/2').json())
print(get('http://127.0.0.1:5000/dialogues/1').json())
print(get('http://127.0.0.1:5000/dialogues').json())
