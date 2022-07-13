import datetime
import json

import requests


def print_help(*params):  # вывод сообщения с доступными командами #TODO: сделать нормальный перенос
    text = "\nPrint '/help' to get help.\n/test - test connection to the server\n/auth [username] [password] - " \
           "authentication to the server\n/get_users - print dictionary with users from database\n/add_user [name] [" \
           "password] [is_admin] - adding new user to the database with users\n" \
           "/delete_user [id] - deleting user from " \
           "database with users\n/log_out - log out from the current user\n/exit - exit the program\n/delay - get request delay to server "
    print(text)


# TODO: Изменить адрес и порт на переменные
#TODO: переписать функции под нужные параметры
#TODO: переписать возвращаемые значения
#TODO: указать типы
#TODO: исправить бред с индексами
def get_delay(*params):
    starting_time = datetime.datetime.now()
    test_request()
    delta = datetime.datetime.now() - starting_time
    print(f"Delay: {delta.microseconds // 1000} ms")

def test_request(*params):  # проверка доступа к серверу
    print("Trying to connect...")
    response = requests.get('http://127.0.0.1:9999/test')
    if bool(response.text): #TODO: проверить это
        print("Successful request to server!!!")
    else:
        print("Invalid request to server...")
    return response.text

def auth(params):  # запрос аутентификации
    name, password = params[:2]
    print(f"Auth user {name} with password {password}")
    if password is not None:
        response = requests.post('http://127.0.0.1:9999/auth/', json={"name": name, "password": password})
        if response.text.strip("\"") == '':
            print("Incorrect name or password!")
        else:
            print(f"Correct authentication! Token {response.text}")
        token = response.text
        return token
    else:
        print("Incorrect parameters!!!")
        return ''


def test_token(token):  # проверка токена доступа
    response = requests.get("http://127.0.0.1:9999/test_token", json={"token": token})
    if bool(response): #TODO: проверить это
        print("Correct access token!")
    else:
        print("Incorrect access token!")


def get_users(params: list):  # получение списка всех пользователей
    # print(params)
    token = params[::-1][0]
    print(f"Get users with token {token}")
    response = requests.get("http://127.0.0.1:9999/get_users", json={"token": token})
    if response.text != "null":
        users_list = json.loads(response.text)
        for user in users_list:
            print(user)
    else:
        print("Incorrect access token!")


def add_user(params):  # запрос на добавление нового пользователя
    print(params)
    name, password, is_admin = params[:3]
    token = params[::-1][0]
    print(token, name, password, is_admin)
    response = requests.get(
        "http://127.0.0.1:9999/add_user",
        json={"token": token, "name": name, "password": password, "is_admin": is_admin}
    )
    print(response.text)


def log_out(params):  # запрос на отключение токена доступа
    token = params[::-1][0]
    requests.get("http://127.0.0.1:9999/log_out", json={"token": token})
    print("Logged out...")


def delete_user(params):  # запрос на удаление пользователя
    id_user = params[0]
    token = params[::-1][0]
    print(f"Deleting request: token {token}, id_user {id_user}")
    response = requests.get("http://127.0.0.1:9999/delete_user", json={"token": token, "id": id_user})
    print(response.text)
