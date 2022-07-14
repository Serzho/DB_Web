import datetime
import json
import requests


class CommandHandler:
    commands_dict = None
    token = None
    ip = None
    port = None

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "9999"
        self.token = ''
        self.commands_dict = {  # TODO: переделать
            "/help": {"f_name": self.print_help, "argv": ()},
            "/test": {"f_name": self.test_request, "argv": ()},
            "/auth": {"f_name": self.auth, "argv": ("name", "password")},
            "/test_token": {"f_name": self.test_token, "argv": ()},
            "/get_users": {"f_name": self.get_users, "argv": ()},
            "/add_user": {"f_name": self.add_user, "argv": ("name", "password", "False")},
            "/delete_user": {"f_name": self.delete_user, "argv": ("0",)},
            "/log_out": {"f_name": self.log_out, "argv": ()},
            "/delay": {"f_name": self.get_delay, "argv": ()}
        }  # словарь доступных команд

    def input_command(self) -> {str: list}:
        input_string = input().split()
        user_input = {"command": input_string.pop(0)}
        if len(input_string):
            user_input.update({"argv": input_string})
        else:
            user_input.update({"argv": []})
        print(user_input.get("command"), user_input.get("argv"))
        return user_input

    def run_command(self, user_input: {str: list}):
        if len(user_input.get("argv")) != len(self.commands_dict.get(user_input.get("command")).get("argv")):
            print("Invalid parameter")
        else:
            self.commands_dict.get(
                user_input.get("command")
            ).get("f_name")(*user_input.get("argv"))

    def print_help(self):  # вывод сообщения с доступными командами
        text = "\nPrint '/help' to get help." \
               "\n/test - test connection to the server" \
               "\n/auth [username] [password] - authentication to the server" \
               "\n/get_users - print dictionary with users from database" \
               "\n/add_user [name] [password] [is_admin (True/False)] - adding new user to the database with users" \
               "\n/delete_user [id] - deleting user from database with users" \
               "\n/log_out - log out from the current user" \
               "\n/exit - exit the program" \
               "\n/delay - get request delay to server "
        print(text)

    # TODO: Изменить адрес и порт на переменные
    # TODO: переписать возвращаемые значения
    # TODO: указать типы

    def get_delay(self):
        starting_time = datetime.datetime.now()
        self.test_request()
        delta = datetime.datetime.now() - starting_time
        print(f"Delay: {delta.microseconds // 1000} ms")

    def test_request(self):  # проверка доступа к серверу
        print("Trying to connect...")
        response = requests.get(f'http://{self.ip}:{self.port}/test')
        if bool(response.text):  # TODO: проверить это
            print("Successful request to server!!!")
        else:
            print("Invalid request to server...")
        return response.text

    def auth(self, name, password):  # запрос аутентификации
        print(f"Auth user {name} with password {password}")
        if password is not "password":
            response = requests.post(
                f'http://{self.ip}:{self.port}/auth/',
                json={"name": name, "password": password}
            )
            if response.text.strip("\"") == '':
                print("Incorrect name or password!")
            else:
                print(f"Correct authentication! Token {response.text}")
            self.token = response.text
        else:
            print("Incorrect parameters!!!")

    def test_token(self):  # проверка токена доступа
        response = requests.get(
            f'http://{self.ip}:{self.port}/test_token',
            json={"token": self.token}
        )
        if bool(response):  # TODO: проверить это
            print("Correct access token!")
        else:
            print("Incorrect access token!")

    def get_users(self):  # получение списка всех пользователей
        print(f"Get users with token {self.token}")
        response = requests.get(
            f'http://{self.ip}:{self.port}/get_users',
            json={"token": self.token}
        )
        if response.text != "null":
            users_list = json.loads(response.text)
            for user in users_list:
                print(user)
        else:
            print("Incorrect access token!")

    def add_user(self, name, password, is_admin):  # запрос на добавление нового пользователя
        print(self.token, name, password, is_admin)
        response = requests.get(
            f'http://{self.ip}:{self.port}/add_user',
            json={"token": self.token, "name": name, "password": password, "is_admin": is_admin}
        )
        print(response.text)

    def log_out(self):  # запрос на отключение токена доступа
        requests.get(
            f'http://{self.ip}:{self.port}/log_out',
            json={"token": self.token}
        )
        print("Logged out...")

    def delete_user(self, id_user):  # запрос на удаление пользователя
        print(f"Deleting request: token {self.token}, id_user {id_user}")
        response = requests.get(
            f'http://{self.ip}:{self.port}/delete_user',
            json={"token": self.token, "id": id_user}
        )
        print(response.text)
