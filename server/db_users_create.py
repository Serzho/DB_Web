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
    with open("tmp/database.db", "ab") as f:
        print("Opened database.db")
        db_users_loaded = True
        f.close()


class User(Base):  # модель базы данных пользователей
    __tablename__ = 'users'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    is_admin = sqlalchemy.Column("is_admin", sqlalchemy.Boolean)
    name = sqlalchemy.Column("name", sqlalchemy.String(100))
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String())
    is_active = sqlalchemy.Column(
        "is_active",
        sqlalchemy.Boolean(),
    )
    access_token = sqlalchemy.Column("access_token", sqlalchemy.String())

    def __init__(self, id, is_admin, name, hashed_password, is_active, access_token):
        self.id = id
        self.is_admin = is_admin
        self.name = name
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.access_token = access_token

