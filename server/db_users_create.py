import os.path

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# проверка существования базы данных
if not os.path.exists("tmp/database.db"):
    with open("tmp/database.db", "wb") as f:
        # создание базы данных
        print("Database.db is not found!!!\nCreated database.db")
        db_users_loaded = False
        f.close()

else:
    # пробное открытие базы данных
    with open("tmp/database.db", "ab") as f:
        print("Opened database.db")
        db_users_loaded = True
        f.close()


class User(Base):  # модель базы данных пользователей
    __tablename__ = 'user'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id (номер) пользователя
    is_admin = sqlalchemy.Column("is_admin", sqlalchemy.Boolean)  # наличие прав администратора
    name = sqlalchemy.Column("name", sqlalchemy.String(100))  # имя пользователя
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String(32))  # пароль в хешируемом виде
    is_active = sqlalchemy.Column(  # есть ли созданный токен (активно ли подключение пользователя)
        "is_active",
        sqlalchemy.Boolean(),
    )
    access_token = sqlalchemy.Column("access_token", sqlalchemy.String(32))  #  токен доступа


    def __init__(self, is_admin: bool, name: str, hashed_password: str, is_active: bool, access_token: str):
        self.is_admin = is_admin
        self.name = name
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.access_token = access_token

    def get_dict(self) -> dict:
        returning_dict = {
            "is_admin": self.is_admin,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "access_token": self.access_token,
        }
        return returning_dict