import os.path

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
NAME_MAX_LENGTH = 100
#TODO: закинуть это в служебное и убрать такой бред отсюда
#TODO: переделтаь под модуль PATH
# проверка существования базы данных
# def db_exists():



class User(Base):  # модель базы данных пользователей
    __tablename__ = 'user'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id (номер) пользователя
    is_admin = sqlalchemy.Column("is_admin", sqlalchemy.Boolean)  # наличие прав администратора
    name = sqlalchemy.Column("name", sqlalchemy.String(NAME_MAX_LENGTH))  # имя пользователя#TODO: проверить ограничение
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String(32))  # пароль в хешируемом виде #TODO: вынести константы
    is_active = sqlalchemy.Column(  # есть ли созданный токен (активно ли подключение пользователя) #TODO: бесполезно, убрать
        "is_active",
        sqlalchemy.Boolean(),
    )



    def __init__(self, is_admin: bool, name: str, hashed_password: str, is_active: bool): #TODO: проверить нужно ли это
        self.is_admin = is_admin
        self.name = name
        self.hashed_password = hashed_password
        self.is_active = is_active

    def get_dict(self) -> dict:
        returning_dict = {
            "id": self.id,
            "is_admin": self.is_admin,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
        }
        return returning_dict


class Token(Base):
    __tablename__ = 'token'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)  # id (номер) пользователя
    access_token = sqlalchemy.Column("access_token", sqlalchemy.String(32))  # токен доступа
    time_creation = sqlalchemy.Column("time_creation", sqlalchemy.Integer) #TODO: переделать на дейттайм

    def __init__(self, id: int, access_token: str, time_creation: int): #TODO: нужно ли это?
        self.id = id
        self.access_token = access_token
        self.time_creation = time_creation

    def get_dict(self) -> dict:
        returning_dict = {
            "id": self.id,
            "access_token": self.access_token,
            "time_creation": self.time_creation,
        }
        return returning_dict
