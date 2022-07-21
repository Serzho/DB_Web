import datetime

import sqlalchemy
from service import Base_auth


class Token(Base_auth):
    __tablename__ = 'token'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True)
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
