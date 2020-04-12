"""ФАЙЛ ДЛЯ ТЕСТИРОВАНИЯ РАБОТЫ БАЗЫ ДАННЫХ."""

# Импорты необходимых библиотек, классов и функций
from requests import get, post, delete
from server import PORT

# Корректные запросы
print('Корректные запросы\n')
# Для пользователей
print('Для пользователя')
print(post(f'http://localhost:{PORT}/users', json={
    'login': '1',
    'name': '1',
    'surname': '1',
    'age': 1,
    'about': '1',
    'password': '1'
}).json())
print(post(f'http://localhost:{PORT}/users', json={
    'login': '2',
    'name': '2',
    'surname': '2',
    'age': 2,
    'about': '2',
    'password': '2'
}).json())
print(post(f'http://localhost:{PORT}/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'age': 3,
    'about': '3',
    'password': '3'
}).json())
print(get(f'http://localhost:{PORT}/users').json())
print(delete(f'http://localhost:{PORT}/users/3').json())
print(get(f'http://localhost:{PORT}/users/1').json())
print(get(f'http://localhost:{PORT}/users/2').json())
print(get(f'http://localhost:{PORT}/users').json())
print()
# Для новостей
print('Для новостей')
print(post(f'http://localhost:{PORT}/news', json={
    'title': 'Test news 1',
    'content': 'this is test news 1',
    'is_private': False,
    'user_id': 1
}).json())
print(post(f'http://localhost:{PORT}/news', json={
    'title': 'Test news 2',
    'content': 'this is test news 2',
    'is_private': True,
    'user_id': 2
}).json())
print(get(f'http://localhost:{PORT}/news').json())
print(get(f'http://localhost:{PORT}/news/1').json())
print(get(f'http://localhost:{PORT}/news/2').json())
print(delete(f'http://localhost:{PORT}/news/1').json())
print(get(f'http://localhost:{PORT}/news').json())
print()
# Для диалогов
print('Для диалогов')
print(post(f'http://localhost:{PORT}/dialogues', json={
    'name': 'Test dialog 1',
    'members': [1, 2]
}).json())
print(post(f'http://localhost:{PORT}/dialogues', json={
    'name': 'Test dialog 2',
    'members': [1, 2]
}).json())
print(get(f'http://localhost:{PORT}/dialogues').json())
print(delete(f'http://localhost:{PORT}/dialogues/2').json())
print(get(f'http://localhost:{PORT}/dialogues/1').json())
print(get(f'http://localhost:{PORT}/dialogues').json())
print()
# Для сообщений
print('Для сообщений')
print(post(f'http://localhost:{PORT}/messages', json={
    'text': 'Test message 1',
    'user_id': 1,
    'dialogue_id': 1
}).json())
print(post(f'http://localhost:{PORT}/messages', json={
    'text': 'Test message 2',
    'user_id': 2,
    'dialogue_id': 1
}).json())
print(get(f'http://localhost:{PORT}/messages').json())
print(get(f'http://localhost:{PORT}/messages/1').json())
print(get(f'http://localhost:{PORT}/messages/2').json())
print(delete(f'http://localhost:{PORT}/messages/1').json())
print(get(f'http://localhost:{PORT}/messages').json())
print()

# Некорректные запросы
print('Некорректные запросы\n')
# Для пользователей
print('Для пользователей')
print(post(f'http://localhost:{PORT}/users', json={
    'login': '1',
    'name': '3',
    'surname': '3',
    'age': 3,
    'about': '3',
    'password': '3'
}).json())
print(post(f'http://localhost:{PORT}/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'about': '3',
    'password': '3'
}).json())
print(post(f'http://localhost:{PORT}/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'age': 'adsfs',
    'about': '3',
    'password': '3'
}).json())
print(delete(f'http://localhost:{PORT}/users/3').json())
print(get(f'http://localhost:{PORT}/users/3').json())
# print(get(f'http://localhost:{PORT}/users/asd').json())
print()
# Для новостей
print('Для новостей')
print(post(f'http://localhost:{PORT}/news', json={
    'title': 'Test news 1',
    'is_private': False,
    'user_id': 1
}).json())
print(post(f'http://localhost:{PORT}/news', json={
    'title': 'Test news 2',
    'content': 'this is test news 2',
    'is_private': False,
    'user_id': 'asd'
}).json())
print(get(f'http://localhost:{PORT}/news/999').json())
# print(get(f'http://localhost:{PORT}/news/asd').json())
print(delete(f'http://localhost:{PORT}/news/999').json())
print()
# Для диалогов
print('Для диалогов')
print(post(f'http://localhost:{PORT}/dialogues', json={
    'name': 'Test dialog 1',
    'members': [1, 'asd']
}).json())
print(post(f'http://localhost:{PORT}/dialogues', json={
    'members': [1, 2]
}).json())
print(delete(f'http://localhost:{PORT}/dialogues/999').json())
print(get(f'http://localhost:{PORT}/dialogues/999').json())
# print(get(f'http://localhost:{PORT}/dialogues/asd').json())
print()
# Для сообщений
print('Для сообщений')
print(post(f'http://localhost:{PORT}/messages', json={
    'text': 'Test message 1',
    'dialogue_id': 1
}).json())
print(post(f'http://localhost:{PORT}/messages', json={
    'text': 'Test message 2',
    'user_id': 'sdf',
    'dialogue_id': 1
}).json())
print(post(f'http://localhost:{PORT}/messages', json={
    'text': 'Test message 2',
    'user_id': 1,
    'dialogue_id': 'asd'
}).json())
print(get(f'http://localhost:{PORT}/messages/999').json())
# print(get(f'http://localhost:{PORT}/messages/asd').json())
print(delete(f'http://localhost:{PORT}/messages/999').json())
print()
