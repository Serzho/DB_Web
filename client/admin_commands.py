import requests


def print_help():  # вывод сообщения с доступными командами
    text = "\nPrint '/help' to get help.\n/test - test connection to the server\n/auth [username] [password] - " \
           "authentication to the server\n/get_users - print dictionary with users from database\n/add_user [name] [" \
           "password] [is_admin] - adding new user to the database with users\n" \
           "/delete_user [id] - deleting user from " \
           "database with users\n/log_out - log out from the current user\n/exit - exit the program "
    print(text)


def test_request():  # проверка доступа к серверу
    print("Trying to connect...")
    response = requests.get('http://127.0.0.1:9999/test')
    if bool(response.text):
        print("Successful request to server!!!")
    else:
        print("Invalid request to server...")
    return response.text


def auth(name=None, password=None):  # запрос аутентификации
    if password is not None:
        response = requests.post('http://127.0.0.1:9999/auth/', json={"name": name, "password": password})
        if response.text == "":
            print("Incorrect name or password!")
        else:
            print(f"Correct authentication! Token {response.text}")
        token = response.text
        return token
    else:
        print("Incorrect parameters!!!")
        return ""


def test_token(token):  # проверка токена доступа
    response = requests.get("http://127.0.0.1:9999/test_token", json={"token": token})
    if bool(response):
        print("Correct access token!")
    else:
        print("Incorrect access token!")


def get_users(token):  # получение списка всех пользователей
    response = requests.get("http://127.0.0.1:9999/get_users", json={"token": token})
    if response.text != "null":
        print(response.text)
        return response.text
    else:
        print("Incorrect access token!")
        return None


def add_user(token, name, password, is_admin):  # запрос на добавление нового пользователя
    response = requests.get("http://127.0.0.1:9999/add_user",
                            json={"token": token, "name": name, "password": password, "is_admin": is_admin})
    print(response.text)


def log_out(token):  # запрос на отключение токена доступа
    requests.get("http://127.0.0.1:9999/log_out", json={"token": token})
    print("Log outed...")


def delete_user(token, id_user):  # запрос на удаление пользователя
    response = requests.get("http://127.0.0.1:9999/delete_user", json={"token": token, "id": id_user})
    print(response.text)
