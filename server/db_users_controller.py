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
        password = ""
        is_correct = False
        print("Please, create admin profile: ")
        while not is_correct:  # защищенный ввод пароля с проверкой #TODO: переделать под continue
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
        user = User(id, is_admin, name, hashed_password, is_active, access_token="")
        self.session.add(user)  # добавление пользователя в сессию
        # for el in db.session:
        #     print(el)
        self.session.commit()  # коммит с новым пользователем в базу данных

    def auth_user(self, auth_name: str, auth_password: str) -> (int, str):  # аутентификация пользователя
        hashed_auth_password = hashlib.md5(auth_password.encode()).hexdigest()  # хэширование пароля
        print(f"Try to sign in: {auth_name}, {auth_password}")
        query_names = self.session.query(User.id, User.name, User.hashed_password).all()  # выбор по id, имени и паролю
        id_auth_user = -1 #TODO: убрать этот бред
        for user in query_names:  # проход по списку пользователей
            if user[1] == auth_name and user[2] == hashed_auth_password: #TODO: не работать с индексами
                id_auth_user = user[0]
        token = ""
        if id_auth_user == -1:
            print("Incorrect name or password!")
        else:
            print("Correct!")
            print("Creating access token...")
            token = self.create_token(id_auth_user)  # создание токена доступа
            # добавление токена в словарь контроллера токенов
            self.tokens_controller.tokens_time.update({id_auth_user: datetime.now()})
            print("Token successfully created!")

        return id_auth_user, token

    def create_token(self, id_auth: int) -> str:  # функция создания токена
        token = secrets.token_hex(16)  # получение случайного значения #TODO: исправить безопасность генерации токена
        print(id_auth)
        user = self.session.query(User).filter(User.id == id_auth).first()
        print(user, type(user))
        user.is_active = True  # измение статуса соединения на "активное"
        user.access_token = token  # добавление токена
        self.session.commit()  # коммит изменений

        return token

    def delete_token(self, id_token: int):
        user = self.session.query(User).filter(User.id == id_token).first()
        user.is_active = False
        user.access_token = ""
        temp = self.tokens_controller.tokens_time.get(id_token)
        del temp #TODO: переделать
        self.session.commit()

    def stop_tokens_controller(self):  # функция остановки контроллера токенов
        self.tokens_controller.is_running = False
        self.tokens_controller.join() #TODO: проверить нужно ли это

    def check_token_exists(self, token) -> bool:  # функция проверки существования токена
        tokens_list = self.session.query(User.access_token).filter(User.access_token == token.strip("\"")).all()
        return len(tokens_list) > 0 #TODO: переделать под count()

    def get_users_dict(self) -> list:  # функция получения списка всех пользователей
        returning_dict = []
        for row in self.session.query(User).all():  # проход по всем строкам в базе данных
            returning_dict.append(row.__dict__)  # добавление строк из базы данных в виде словаря в выходной список #TODO: переписать дикт под себя
        # print(returning_dict)
        return returning_dict

    def check_token_admin(self, token) -> bool:  # проверка токена на права доступа администратора
        tokens_list = self.session.query(User.access_token, User.is_admin).filter(
            User.access_token == token.strip("\""),
            User.is_admin == bool(1) #TODO: исправить костыль
        ).all()
        return len(tokens_list) > 0

    def next_user_id(self) -> int:  # получение следующего незанятого id #TODO: УБРАТЬ ЭТО ВООБЩЕ
        temp = self.session.query(User.id).all()[::-1]
        return temp[0][0] + 1

    def clear_access_tokens(self):  # функция удаления всех токенов доступа
        for i in range(self.next_user_id()):
            try:
                self.delete_token(i)
            except AttributeError:
                pass

    def id_of_token(self, token: str) -> int:  # получение id по токену
        tokens_list = self.session.query(User.id, User.access_token).filter(
            User.access_token == token.strip("\"")).first() #TODO: исправить работу с индексами, кавычки
        print(f"id of token {list(tokens_list)[0]}")
        return list(tokens_list)[0] #TODO: сделать перепроверку существования

    def delete_user(self, id_user):  # функция удаления пользователя
        self.delete_token(id_user)  # удаление токена доступа пользователя
        user = self.session.query(User).filter(User.id == id_user)
        user.delete() #TODO: попробовать удалить с помощью метода session
        self.session.commit()
