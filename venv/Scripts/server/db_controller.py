import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import *

from db_create import db
from db_create import User

Base = declarative_base()


class DB_Controller:
    metadata = None

    def __init__(self):
        print("Creating users table...")
        db.create_all()
        print("Successful creating!")
        self.add_user(id=0, is_admin=True, name="admin", hashed_password="12345")

    def add_user(self, id: int, name: str, hashed_password: str, is_admin=False, is_active=False):
        user = User(id, is_admin, name, hashed_password, is_active)
        db.session.add(user)
        for el in db.session:
            print(el)
        db.session.commit()
