import hashlib
from getpass import getpass

import sqlalchemy
from sqlalchemy.orm import *

from db_users_create import User, db_users_loaded, Base


class DB_Users_Controller:
    session = None
    def __init__(self):
        print("Creating users table...")
        engine = sqlalchemy.create_engine("sqlite:///tmp/database.db")
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)
        print("Successful creating!")
        if not db_users_loaded:
            self.create_main_admin()

        # self.get()

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
        self.session.add(user)
        # for el in db.session:
        #     print(el)
        self.session.commit()
