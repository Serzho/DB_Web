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
        self.commands_dict = {
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

    def get_delay(self):
        starting_time = datetime.datetime.now()
        self.test_request()
        delta = datetime.datetime.now() - starting_time
        print(f"Delay: {delta.microseconds // 1000} ms")

    def test_request(self) -> bool:  # проверка доступа к серверу
        print("Trying to connect...")
        response = requests.get(f'http://{self.ip}:{self.port}/test')
        print(json.loads(response.content).get("success"))
        success = bool(json.loads(response.content).get("success"))
        if success:
            print("Successful request to server!!!")
        else:
            print("Invalid request to server...")
        return success

    def auth(self, name: str, password: str):  # запрос аутентификации
        print(f"Auth user {name} with password {password}")
        if password is not "password":
            response = requests.get(
                f'http://{self.ip}:{self.port}/auth/',
                json={"name": name, "password": password}
            )
            success = bool(json.loads(response.content).get("success"))
            if success:
                token = json.loads(response.content).get("data")
                print(f"Correct authentication! Token {token}")
                self.token = token
            else:
                print("Incorrect name or password!")
        else:
            print("Incorrect parameters!!!")

    def test_token(self):  # проверка токена доступа
        response = requests.get(
            f'http://{self.ip}:{self.port}/test_token',
            json={"token": self.token}
        )
        success = json.loads(response.content).get("success")
        if success:
            print("Correct access token!")
        else:
            print("Incorrect access token!")

    def get_users(self):  # получение списка всех пользователей
        print(f"Get users with token {self.token}")
        response = requests.get(
            f'http://{self.ip}:{self.port}/get_users',
            json={"token": self.token}
        )
        success = json.loads(response.content).get("success")
        if success:
            users_list = json.loads(response.content).get("data")
            for user in users_list:
                print(user)
        else:
            print("Incorrect access token!")

    def add_user(self, name: str, password: str, is_admin: str):  # запрос на добавление нового пользователя
        print(self.token, name, password, is_admin)
        response = requests.get(
            f'http://{self.ip}:{self.port}/add_user',
            json={"token": self.token, "name": name, "password": password, "is_admin": is_admin}
        )
        success = json.loads(response.content).get("success")
        if success:
            print("User was added:")
            print((json.loads(response.content).get("data")))
        else:
            print("Error: ")
            print((json.loads(response.content).get("data")))

    def log_out(self):  # запрос на отключение токена доступа
        requests.get(
            f'http://{self.ip}:{self.port}/log_out',
            json={"token": self.token}
        )
        print("Logged out...")

    def delete_user(self, id_user: str):  # запрос на удаление пользователя
        print(f"Deleting request: token {self.token}, id_user {id_user}")
        response = requests.get(
            f'http://{self.ip}:{self.port}/delete_user',
            json={"token": self.token, "id": id_user}
        )
        print((json.loads(response.content).get("data")))