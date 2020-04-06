"""ФАЙЛ ДЛЯ ТЕСТИРОВАНИЯ РАБОТЫ БАЗЫ ДАННЫХ."""

# Импорты необходимых библиотек, классов и функций
from requests import get, post, delete

# Корректные запросы
print('Корректные запросы\n')
# Для пользователей
print('Для пользователя')
print(post('http://127.0.0.1:5000/users', json={
    'login': '1',
    'name': '1',
    'surname': '1',
    'age': 1,
    'about': '1',
    'password': '1'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '2',
    'name': '2',
    'surname': '2',
    'age': 2,
    'about': '2',
    'password': '2'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'age': 3,
    'about': '3',
    'password': '3'
}).json())
print(get('http://127.0.0.1:5000/users').json())
print(delete('http://127.0.0.1:5000/users/3').json())
print(get('http://127.0.0.1:5000/users/1').json())
print(get('http://127.0.0.1:5000/users/2').json())
print(get('http://127.0.0.1:5000/users').json())
print()
# Для новостей
print('Для новостей')
print(post('http://127.0.0.1:5000/news', json={
    'title': 'Test news 1',
    'content': 'this is test news 1',
    'is_private': False,
    'user_id': 1
}).json())
print(post('http://127.0.0.1:5000/news', json={
    'title': 'Test news 2',
    'content': 'this is test news 2',
    'is_private': True,
    'user_id': 2
}).json())
print(get('http://127.0.0.1:5000/news').json())
print(get('http://127.0.0.1:5000/news/1').json())
print(get('http://127.0.0.1:5000/news/2').json())
print(delete('http://127.0.0.1:5000/news/1').json())
print(get('http://127.0.0.1:5000/news').json())
print()
# Для диалогов
print('Для диалогов')
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
print()
# Для сообщений
print('Для сообщений')
print(post('http://127.0.0.1:5000/messages', json={
    'text': 'Test message 1',
    'user_id': 1,
    'dialogue_id': 1
}).json())
print(post('http://127.0.0.1:5000/messages', json={
    'text': 'Test message 2',
    'user_id': 2,
    'dialogue_id': 1
}).json())
print(get('http://127.0.0.1:5000/messages').json())
print(get('http://127.0.0.1:5000/messages/1').json())
print(get('http://127.0.0.1:5000/messages/2').json())
print(delete('http://127.0.0.1:5000/messages/1').json())
print(get('http://127.0.0.1:5000/messages').json())
print()

# Некорректные запросы
print('Некорректные запросы\n')
# Для пользователей
print('Для пользователей')
print(post('http://127.0.0.1:5000/users', json={
    'login': '1',
    'name': '3',
    'surname': '3',
    'age': 3,
    'about': '3',
    'password': '3'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'about': '3',
    'password': '3'
}).json())
print(post('http://127.0.0.1:5000/users', json={
    'login': '3',
    'name': '3',
    'surname': '3',
    'age': 'adsfs',
    'about': '3',
    'password': '3'
}).json())
print(delete('http://127.0.0.1:5000/users/3').json())
print(get('http://127.0.0.1:5000/users/3').json())
# print(get('http://127.0.0.1:5000/users/asd').json())
print()
# Для новостей
print('Для новостей')
print(post('http://127.0.0.1:5000/news', json={
    'title': 'Test news 1',
    'is_private': False,
    'user_id': 1
}).json())
print(post('http://127.0.0.1:5000/news', json={
    'title': 'Test news 2',
    'content': 'this is test news 2',
    'is_private': False,
    'user_id': 'asd'
}).json())
print(get('http://127.0.0.1:5000/news/999').json())
# print(get('http://127.0.0.1:5000/news/asd').json())
print(delete('http://127.0.0.1:5000/news/999').json())
print()
# Для диалогов
print('Для диалогов')
print(post('http://127.0.0.1:5000/dialogues', json={
    'name': 'Test dialog 1',
    'members': [1, 'asd']
}).json())
print(post('http://127.0.0.1:5000/dialogues', json={
    'members': [1, 2]
}).json())
print(delete('http://127.0.0.1:5000/dialogues/999').json())
print(get('http://127.0.0.1:5000/dialogues/999').json())
# print(get('http://127.0.0.1:5000/dialogues/asd').json())
print()
# Для сообщений
print('Для сообщений')
print(post('http://127.0.0.1:5000/messages', json={
    'text': 'Test message 1',
    'dialogue_id': 1
}).json())
print(post('http://127.0.0.1:5000/messages', json={
    'text': 'Test message 2',
    'user_id': 'sdf',
    'dialogue_id': 1
}).json())
print(post('http://127.0.0.1:5000/messages', json={
    'text': 'Test message 2',
    'user_id': 1,
    'dialogue_id': 'asd'
}).json())
print(get('http://127.0.0.1:5000/messages/999').json())
# print(get('http://127.0.0.1:5000/messages/asd').json())
print(delete('http://127.0.0.1:5000/messages/999').json())
print()
