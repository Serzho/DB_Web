import hashlib

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import *
from getpass import getpass
from db_create import db
from db_create import User

Base = declarative_base()


class DB_Controller:
    metadata = None

    def __init__(self):
        print("Creating users table...")
        db.create_all()
        print("Successful creating!")
        self.create_main_admin()

    def create_main_admin(self):
        password = ""
        is_correct = False
        print("Please, create admin profile: ")
        while not is_correct:
            print("\nEnter the password: ")
            password = getpass()
            print("Re-enter the password: ")
            if password == getpass():
                print("Correct password!")
                is_correct = True
            else:
                print("Passwords do not match!")
        self.add_user(id=0, is_admin=True, name="admin", password=password)
        print("Successfully creating admin!")


    def add_user(self, id: int, name: str, password: str, is_admin=False, is_active=False):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = User(id, is_admin, name, hashed_password, is_active)
        db.session.add(user)
        for el in db.session:
            print(el)
        db.session.commit()
