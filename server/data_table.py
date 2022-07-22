import datetime

import sqlalchemy
from service import Base_db


class Data(Base_db):
    __tablename__ = 'data'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column("author_id", sqlalchemy.Integer)
    key = sqlalchemy.Column("key", sqlalchemy.String(100))
    value = sqlalchemy.Column("value", sqlalchemy.String(100))
    time_creation = sqlalchemy.Column("time_creation", sqlalchemy.DateTime)

    def __init__(self, author_id: int, key: str, value: str, time_creation: datetime):
        self.author_id = author_id
        self.key = key
        self.value = value
        self.time_creation = time_creation
