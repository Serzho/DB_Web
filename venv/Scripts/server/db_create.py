from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Callable


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Boolean: Callable


app = Flask(__name__)
with open("tmp/database.db", "wb") as f:
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = MySQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    is_admin = db.Column("is_admin", db.Boolean)
    name = db.Column("name", db.String(100))
    hashed_password = db.Column("hashed_password", db.String())
    is_active = db.Column(
        "is_active",
        db.Boolean(),
    )

    def __init__(self, id, is_admin, name, hashed_password, is_active):
        self.id = id
        self.is_admin = is_admin
        self.name = name
        self.hashed_password = hashed_password
        self.is_active = is_active
