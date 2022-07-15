import hashlib
from getpass import getpass
# TODO: исправить порядок модулей
import sqlalchemy
from sqlalchemy.orm import *

from db_users_create import User, Base, Token
import secrets
from tokens_controller import TokensController
from datetime import datetime
from pathlib import Path


class DBUsersController:  # класс контроллера базы данных пользователя
    session = None
    tokens_controller = None

    # TODO: исправить названия
    # TODO: исправить ошибки в английских словах
    # TODO: сделать нормальный формат
    # TODO: сделать логирование
    def __init__(self):
        print("Creating users table...")
        db_exists = Path.exists(Path("tmp/database.db"))
        engine = sqlalchemy.create_engine(
            "sqlite:///tmp/database.db?check_same_thread=False")  # создание движка базы данных
        Base.metadata.create_all(engine)  # создание баззы данных
        self.session = Session(bind=engine)  # создание сессии базы данных
        print("Successful creating!")
        if not db_exists:  # создание учетной записи администратора при создании новой бд
            self.create_main_admin()
        self.tokens_controller = TokensController(self)  # создание контроллера токеов
        self.tokens_controller.start()  # запуск контроллера токенов
        self.delete_all_tokens()  # очистка всех токенов при открытии базы данных

    def create_main_admin(self):  # создание первого администратора
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

    def add_user(self, name: str, password: str, is_admin=False):  # создание нового пользователя
        hashed_password = hashlib.md5(password.encode()).hexdigest()  # хэширование пароля
        user = User(is_admin, name, hashed_password)
        self.session.add(user)  # добавление пользователя в сессию
        self.session.commit()  # коммит с новым пользователем в базу данных

    def auth_user(self, auth_name: str, auth_password: str) -> (int, str):  # аутентификация пользователя
        hashed_auth_password = hashlib.md5(auth_password.encode()).hexdigest()  # хэширование пароля
        print(f"Try to sign in: {auth_name}, {auth_password}")
        id_auth_user, token = None, None
        user = self.session.query(
            User.name, User.hashed_password, User.id
        ).filter(
            User.name == auth_name,
            User.hashed_password == hashed_auth_password
        ).first()
        if user is not None:
            id_auth_user = user.id
            print("Correct!")
            print("Creating access token...")
            token = self.create_token(id_auth_user)  # создание токена доступа
            print("Token successfully created!")
        else:
            print("Incorrect name or password!")
        return id_auth_user, token

    def tokens_time(self):
        tokens_list = []
        for row in self.session.query(Token.id, Token.time_creation).all():
            tokens_list.append({"id": row.id, "time_creation": row.time_creation})
        return tokens_list

    def create_token(self, id_auth: int) -> str:  # функция создания токена
        token = secrets.token_hex(16)  # получение случайного значения
        print(f"Id of token {id_auth}")
        users_id = self.session.query(User.id)
        for user in users_id:
            if user.id != id_auth:
                continue
            print(user, type(user))
            time_creation = datetime.now()
            print(id_auth, token, time_creation)
            last_user_token = self.session.query(Token).first()
            if last_user_token is not None:
                self.session.delete(last_user_token)
            token_row = Token(id_auth, token, time_creation)
            self.session.add(token_row)
            self.session.commit()
        self.session.commit()  # коммит изменений

        return token

    def delete_token(self, id_token: int):
        query_names = self.session.query(User.id).all()
        for user in query_names:
            if user.id == id_token:
                token_row = self.session.query(Token).filter(Token.id == id_token).first()
                if token_row is not None:
                    self.session.delete(token_row)
                self.session.commit()
                break

    def stop_tokens_controller(self):  # функция остановки контроллера токенов
        self.tokens_controller.is_running = False
        self.tokens_controller.join()
        print("Stopped tokens controller!!!")

    def token_exists(self, token) -> bool:  # функция проверки существования токена
        print(f"Cheking token {token}...")
        tokens_list = self.session.query(
            Token.access_token
        ).filter(
            Token.access_token == token.strip("\"")
        ).count()
        return bool(tokens_list > 0) and token != ''

    def users_list(self) -> list:  # функция получения списка всех пользователей
        returning_list = []
        for row in self.session.query(User).all():  # проход по всем строкам в базе данных
            print(type(row))
            user_dict = row.get_dict()
            token = self.session.query(Token).filter(
                Token.id == row.id
            ).first()
            if token is not None:
                user_dict.update({"access_token": token.access_token, "time_creation": str(token.time_creation)})
            returning_list.append(user_dict)

        # print(returning_dict)
        return returning_list

    def token_is_admin(self, token: str) -> bool:  # проверка токена на права доступа администратора
        token = self.session.query(
            Token.access_token, Token.id
        ).filter(
            Token.access_token == token.strip("\""),
        ).first()
        if token is None:
            return False
        admins_list = self.session.query(
            User.id, User.is_admin
        ).filter(
            User.is_admin.is_(True),
            User.id == token.id
        ).all()
        return bool(admins_list)

    def delete_all_tokens(self):  # функция удаления всех токенов доступа
        for user in self.session.query(User).all():
            print(f"Id of token to delete: {user.id} by clear_access_tokens")
            self.delete_token(user.id)

    def get_token_id(self, token: str) -> int:  # получение id по токену
        tokens_user = self.session.query(
            Token.id, Token.access_token
        ).filter(
            Token.access_token == token.strip("\"")
        ).first()
        if tokens_user is not None:
            print(f"id of token {tokens_user.id}")
            return tokens_user.id

    def delete_user(self, id_user):  # функция удаления пользователя
        self.delete_token(id_user)  # удаление токена доступа пользователя
        query_names = self.session.query(User).filter(User.id == id_user)
        for user in query_names:
            if user.id == id_user:
                self.session.delete(user)
                self.session.commit()
                break
