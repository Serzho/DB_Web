import hashlib
from getpass import getpass

import sqlalchemy
from sqlalchemy.orm import *

from db_users_create import User, db_users_loaded, Base
import secrets
from tokens_controller import TokensController
from datetime import  datetime


class DB_Users_Controller:  # класс контроллера базы данных пользователя
    session = None
    tokens_controller = None

    def __init__(self):
        print("Creating users table...")
        engine = sqlalchemy.create_engine("sqlite:///tmp/database.db?check_same_thread=False")  # создание движка базы данных
        Base.metadata.create_all(engine)  # создание баззы данных
        self.session = Session(bind=engine)  # создание сессии базы данных
        print("Successful creating!")
        if not db_users_loaded:  # создание учетной записи администратора при создании новой бд
            self.create_main_admin()
        self.tokens_controller = TokensController(self)
        self.tokens_controller.start()


        # self.get()

    def create_main_admin(self):  # создание первого администратора
        password = ""
        is_correct = False
        print("Please, create admin profile: ")
        while not is_correct:  # защищенный ввод пароля с проверкой
            print("\nEnter the password: ")
            password = getpass()
            print("Re-enter the password: ")
            if password == getpass():
                print("Correct password!")
                is_correct = True
            else:
                print("Passwords do not match!")

        self.add_user(id=0, is_admin=True, name="admin", password=password)  # добавление записи в бд
        print("Successfully creating admin!")

    def add_user(self, id: int, name: str, password: str, is_admin=False,
                 is_active=False):  # создание нового пользователя
        hashed_password = hashlib.md5(password.encode()).hexdigest()  # хэширование пароля
        user = User(id, is_admin, name, hashed_password, is_active, access_token = "")
        self.session.add(user)  # добавление пользователя в сессию
        # for el in db.session:
        #     print(el)
        self.session.commit()  # коммит с новым пользователем в базу данных

    def auth_user(self, auth_name: str, auth_password: str) -> (int, str):
        hashed_auth_password = hashlib.md5(auth_password.encode()).hexdigest()  # хэширование пароля
        print(f"Try to sign in: {auth_name}, {auth_password}")
        query_names = self.session.query(User.id, User.name, User.hashed_password).all()
        id_auth_user = -1
        for user in query_names:
            if user[1] == auth_name and user[2] == hashed_auth_password:
                id_auth_user = user[0]
        token = ""
        if id_auth_user == -1:
            print("Incorrect name or password!")
        else:
            print("Correct!")
            print("Creating access token...")
            token = self.create_token(id_auth_user)
            self.tokens_controller.tokens_time.update({id_auth_user: datetime.now()})
            print("Token successfully created!")

        return id_auth_user, token

    def create_token(self, id_auth: int) -> str:
        token = secrets.token_hex(16)
        print(id_auth)
        user = self.session.query(User).filter(User.id == id_auth).first()
        print(user, type(user))
        user.is_active = True
        user.access_token = token
        self.session.commit()

        return token

    def delete_token(self, id_token: int):
        user = self.session.query(User).filter(User.id == id_token).first()
        user.is_active = False
        user.access_token = ""
        self.session.commit()

    def stop_tokens_controller(self):
        self.tokens_controller.is_running = False
        self.tokens_controller.join()

    def check_token(self, token) -> bool:
        tokens_list = self.session.query(User.access_token).filter(User.access_token == token.strip("\"")).all()
        return len(tokens_list) > 0
