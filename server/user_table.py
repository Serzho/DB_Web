import sqlalchemy
from service import Base_auth

NAME_MAX_LENGTH = 100


class User(Base_auth):  # модель базы данных пользователей
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
