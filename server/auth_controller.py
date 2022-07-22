import hashlib
from getpass import getpass
# TODO: исправить порядок модулей

from user_table import User
from token_table import Token
import secrets
from tokens_controller import TokensController
from datetime import datetime
from service import load_session, base_logger


def log(message):
    module_name = "AUTH CONTROLLER"
    base_logger(msg=message, module_name=module_name)


class AuthController:  # класс контроллера базы данных пользователя
    session = None
    tokens_controller = None

    def __init__(self):
        print("Creating users table...")
        self.session, db_exists = load_session("auth")  # создание сессии базы данных
        print("Successful creating!")
        if not db_exists:  # создание учетной записи администратора при создании новой бд
            self.create_main_admin()
        self.tokens_controller = TokensController(self)  # создание контроллера токеов
        self.tokens_controller.start()  # запуск контроллера токенов
        self.__delete_all_tokens()  # очистка всех токенов при открытии базы данных
        log("Auth controller initialized")

    def create_main_admin(self) -> None:  # создание первого администратора
        log("Creating first admin profile")
        print("Please, create admin profile: ")
        while True:  # защищенный ввод пароля с проверкой
            print("\nEnter the password: ")
            entered_password = getpass()
            print("Re-enter the password: ")
            re_entered_password = getpass()
            if entered_password == re_entered_password:
                print("Correct password!")
                break
            else:
                print("Passwords do not match!")

        self.add_user(is_admin=True, name="admin", password=entered_password)  # добавление записи в бд
        print("Successfully creating admin!")
        log("First admin was created!")

    def add_user(self, name: str, password: str, is_admin=False) -> None:  # создание нового пользователя
        hashed_password = hashlib.md5(password.encode()).hexdigest()  # хэширование пароля
        log(f"Adding user: name = {name}, password = {hashed_password}, is admin = {is_admin}")
        user = User(is_admin, name, hashed_password)
        self.session.add(user)  # добавление пользователя в сессию
        self.session.commit()  # коммит с новым пользователем в базу данных
        log(f"User added!")

    def auth_user(self, auth_name: str, auth_password: str) -> (int, str):  # аутентификация пользователя
        hashed_auth_password = hashlib.md5(auth_password.encode()).hexdigest()  # хэширование пароля
        log(f"Authentication user: name = {auth_name}, password = {hashed_auth_password}")
        print(f"Try to sign in: {auth_name}, {auth_password}")
        id_auth_user, token = None, None
        user = self.session.query(
            User.name, User.hashed_password, User.id
        ).filter(
            User.name == auth_name,
            User.hashed_password == hashed_auth_password
        ).first()
        if user is not None:
            log(f"User found: id = {user.id}")
            id_auth_user = user.id
            print("Correct!")
            print("Creating access token...")
            log(f"Creating access token: id = {user.id}")
            token = self.__create_token(id_auth_user)  # создание токена доступа
            print("Token successfully created!")
            log(f"Correct authentication: id = {user.id}, access token = {token}")
        else:
            print("Incorrect name or password!")
            log(f"Incorrect authentication: name = {auth_name}, password = {hashed_auth_password}")
        return id_auth_user, token

    def tokens_time(self) -> list:
        tokens_list = []
        log("Getting tokens time list...")
        for row in self.session.query(Token.id, Token.time_creation).all():
            tokens_list.append({"id": row.id, "time_creation": row.time_creation})
        return tokens_list

    def __create_token(self, id_auth: int) -> str:  # функция создания токена
        log(f"Creating token with id = {id_auth}")
        token = secrets.token_hex(16)  # получение случайного значения
        print(f"Id of token {id_auth}")
        users_id = self.session.query(User.id)
        for user in users_id:
            if user.id != id_auth:
                continue
            # print(user, type(user))
            time_creation = datetime.now()
            # print(id_auth, token, time_creation)

            last_user_token = self.session.query(Token).first()
            if last_user_token is not None:
                log(f"Deleting last access token: id = {id_auth}")
                self.session.delete(last_user_token)
            log(f"Created token: id = {id_auth}, token = {token}, time creation = {time_creation}")
            token_row = Token(id_auth, token, time_creation)
            self.session.add(token_row)
            self.session.commit()
        self.session.commit()  # коммит изменений

        return token

    def delete_token(self, id_token: int) -> None:
        log(f"Deleting token with id = {id_token}")
        query_names = self.session.query(User.id).all()
        for user in query_names:
            if user.id == id_token:
                token_row = self.session.query(Token).filter(Token.id == id_token).first()
                if token_row is not None:
                    log(f"Token with id = {id_token} was deleted!")
                    self.session.delete(token_row)
                else:
                    log(f"Token not found")
                self.session.commit()
                break

    def stop_tokens_controller(self) -> None:  # функция остановки контроллера токенов
        self.tokens_controller.is_running = False
        self.tokens_controller.join()
        self.__delete_all_tokens()
        print("Stopped tokens controller!!!")
        log("Tokens controller was stopped!!!")

    def token_exists(self, token) -> bool:  # функция проверки существования токена
        print(f"Checking token {token}...")
        log(f"Check existence of token = {token}")
        tokens_list = self.session.query(
            Token.access_token
        ).filter(
            Token.access_token == token.strip("\"")
        ).count()
        log(f"Result: token = {token}, existence = {bool(tokens_list > 0) and token != ''}")
        return bool(tokens_list > 0) and token != ''

    def users_list(self) -> list:  # функция получения списка всех пользователей
        log(f"Getting list of users")
        returning_list = []
        for row in self.session.query(User).all():  # проход по всем строкам в базе данных
            # print(type(row))
            user_dict = row.get_dict()
            token = self.session.query(Token).filter(
                Token.id == row.id
            ).first()
            if token is not None:
                user_dict.update({"access_token": token.access_token, "time_creation": str(token.time_creation)})
            returning_list.append(user_dict)
        log(f"List of users was returned! Rows in list = {len(returning_list)}")
        # print(returning_dict)
        return returning_list

    def token_is_admin(self, token: str) -> bool:  # проверка токена на права доступа администратора
        log(f"Checking admin rights of token = {token}")
        token_row = self.session.query(
            Token.access_token, Token.id
        ).filter(
            Token.access_token == token.strip("\""),
        ).first()
        if token_row is None:
            log(f"Result: token = {token} doesn't have admin rights")
            return False
        admins_list = self.session.query(
            User.id, User.is_admin
        ).filter(
            User.is_admin.is_(True),
            User.id == token_row.id
        ).count()
        log(f"Result: token = {token} have admin rights = {admins_list > 0}")
        return admins_list > 0

    def __delete_all_tokens(self) -> None:  # функция удаления всех токенов доступа
        log(f"Deleting all tokens")
        for user in self.session.query(User).all():
            print(f"Id of token to delete: {user.id} by clear_access_tokens")
            log(f"Id of token to delete: {user.id}")
            self.delete_token(user.id)
        log("All tokens was deleted")

    def get_token_id(self, token: str) -> int:  # получение id по токену
        log(f"Finding id of token: token = {token}")
        tokens_user = self.session.query(
            Token.id, Token.access_token
        ).filter(
            Token.access_token == token.strip("\"")
        ).first()
        if tokens_user is not None:
            log(f"Result: token = {token}, id of token = {tokens_user.id}")
            print(f"id of token {tokens_user.id}")
            return tokens_user.id
        else:
            log(f"Result: id of token = {token} wasn't find!!!")

    def delete_user(self, id_user) -> bool:  # функция удаления пользователя
        log(f"Deleting user with id = {id_user}")
        self.delete_token(id_user)  # удаление токена доступа пользователя
        query_names = self.session.query(User).filter(User.id == id_user)
        for user in query_names:
            if user.id == id_user:
                log(f"User with id = {id_user} was deleted!")
                self.session.delete(user)
                self.session.commit()
                return True
        return False
