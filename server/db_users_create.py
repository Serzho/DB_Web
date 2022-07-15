import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
NAME_MAX_LENGTH = 100

# TODO: сделать связь
class User(Base):  # модель базы данных пользователей
    __tablename__ = 'user'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id (номер) пользователя
    is_admin = sqlalchemy.Column("is_admin", sqlalchemy.Boolean)  # наличие прав администратора
    name = sqlalchemy.Column("name", sqlalchemy.String(NAME_MAX_LENGTH))  # имя пользователя
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String(32))  # пароль в хешируемом виде

    def __init__(self, is_admin: bool, name: str, hashed_password: str):
        self.is_admin = is_admin
        self.name = name
        self.hashed_password = hashed_password

    def get_dict(self) -> dict:
        returning_dict = {
            "id": self.id,
            "is_admin": self.is_admin,
            "name": self.name,
            "hashed_password": self.hashed_password,
        }
        return returning_dict


class Token(Base):
    __tablename__ = 'token'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True)  # id (номер) пользователя
    access_token = sqlalchemy.Column("access_token", sqlalchemy.String(32))  # токен доступа
    time_creation = sqlalchemy.Column("time_creation", sqlalchemy.DateTime)

    def __init__(self, id: int, access_token: str, time_creation: datetime):
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
