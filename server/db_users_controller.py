import hashlib
from getpass import getpass

import sqlalchemy
from sqlalchemy.orm import *

from db_users_create import User, db_users_loaded, Base
import secrets
from tokens_controller import TokensController
from datetime import datetime



class DB_Users_Controller:  # класс контроллера базы данных пользователя
    session = None
    tokens_controller = None

    def __init__(self):
        print("Creating users table...")
        engine = sqlalchemy.create_engine(
            "sqlite:///tmp/database.db?check_same_thread=False")  # создание движка базы данных
        Base.metadata.create_all(engine)  # создание баззы данных
        self.session = Session(bind=engine)  # создание сессии базы данных
        print("Successful creating!")
        if not db_users_loaded:  # создание учетной записи администратора при создании новой бд
            self.create_main_admin()
        self.tokens_controller = TokensController(self)  # создание контроллера токеов
        self.tokens_controller.start()  # запуск контроллера токенов
        self.clear_access_tokens()  # очистка всех токенов при открытии базы данных

        # self.get()

    def create_main_admin(self):  # создание первого администратора
        print("Please, create admin profile: ")
        while True:  # защищенный ввод пароля с проверкой
            print("\nEnter the password: ")
            password = getpass()
            print("Re-enter the password: ")
            if password == getpass():
                print("Correct password!")
                break
            else:
                print("Passwords do not match!")

        self.add_user(is_admin=True, name="admin", password=password)  # добавление записи в бд
        print("Successfully creating admin!")

    def add_user(self, name: str, password: str, is_admin=False,
                 is_active=False):  # создание нового пользователя
        hashed_password = hashlib.md5(password.encode()).hexdigest()  # хэширование пароля
        user = User(is_admin, name, hashed_password, is_active, access_token="")
        self.session.add(user)  # добавление пользователя в сессию
        # for el in db.session:
        #     print(el)
        self.session.commit()  # коммит с новым пользователем в базу данных

    def auth_user(self, auth_name: str, auth_password: str) -> (int, str):  # аутентификация пользователя
        hashed_auth_password = hashlib.md5(auth_password.encode()).hexdigest()  # хэширование пароля
        print(f"Try to sign in: {auth_name}, {auth_password}")
        id_auth_user, token = None, None
        query_names = self.session.query(User).all()
        for user in query_names:  # проход по списку пользователей
            if user.name == auth_name and user.hashed_password == hashed_auth_password:
                id_auth_user = user.id
                print("Correct!")
                print("Creating access token...")
                token = self.create_token(id_auth_user)  # создание токена доступа
                # добавление токена в словарь контроллера токенов
                self.tokens_controller.tokens_time.update({id_auth_user: datetime.now()})
                print("Token successfully created!")
                break
        else:
            print("Incorrect name or password!")
        return id_auth_user, token

    def create_token(self, id_auth: int) -> str:  # функция создания токена
        token = secrets.token_hex(16)  # получение случайного значения
        print(f"Id of token {id_auth}")
        users = self.session.query(User).all()
        for user in users:
            if user.id != id_auth:
                continue
            print(user, type(user))
            user.is_active = True  # измение статуса соединения на "активное"
            user.access_token = token  # добавление токена
        self.session.commit()  # коммит изменений

        return token

    def delete_token(self, id_token: int):
        query_names = self.session.query(User).all()
        for user in query_names:
            if user.id == id_token:
                user.is_active = False
                user.access_token = ""
                del self.tokens_controller.tokens_time[id_token]
                self.session.commit()
                break

    def stop_tokens_controller(self):  # функция остановки контроллера токенов
        self.tokens_controller.is_running = False
        self.tokens_controller.join()
        print("Stopped tokens controller!!!")

    def check_token_exists(self, token) -> bool:  # функция проверки существования токена
        tokens_list = self.session.query(User.access_token).filter(User.access_token == token.strip("\"")).count()
        return bool(tokens_list > 0)

    def get_users_dict(self) -> list:  # функция получения списка всех пользователей
        returning_dict = []
        for row in self.session.query(User).all():  # проход по всем строкам в базе данных
            returning_dict.append(row.__dict__)  # добавление строк из базы данных в виде словаря в выходной список #TODO: переписать дикт под себя
        # print(returning_dict)
        return returning_dict

    def check_token_admin(self, token) -> bool:  # проверка токена на права доступа администратора
        tokens_list = self.session.query(User.access_token, User.is_admin).filter(
            User.access_token == token.strip("\""),
            User.is_admin.is_(True) #TODO: исправить костыль
        ).all()
        return len(tokens_list) > 0

    def clear_access_tokens(self):  # функция удаления всех токенов доступа
        for User.id in self.session.query(User.id).all():
            # print(f"Id of token to delete: {User.id}")
            self.delete_token(User.id)

    def get_token_id(self, token: str) -> int:  # получение id по токену
        tokens_user = self.session.query(User.id, User.access_token).filter(
            User.access_token == token.strip("\"")
        ).first() #TODO: исправить кавычки
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
