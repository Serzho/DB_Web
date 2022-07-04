import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import *

Base = declarative_base()

class DB_Controller():
    metadata = None
    users_base = None
    session = None

    def __init__(self):
        engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts")
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        print("Creating users table...")
        self.users_base = Users_base()
        print("Users table created!")
        self.add_user(id = 0, is_admin=True, name="admin", hashed_password="12345")

    def add_user(self, id: int, name: str, hashed_password: str, is_admin = False,  is_active = False):
        self.session = sqlalchemy.orm.Session()
        user = Users_base(id, is_admin, name, hashed_password, is_active)
        self.session.add(user)
        print(session.new)
        self.session.commit()
        for post in self.session.query(Post):
            print(post)

class Users_base(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    is_admin = sqlalchemy.Column("is_admin", sqlalchemy.Boolean)
    name = sqlalchemy.Column("name", sqlalchemy.String(100))
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String())
    is_active = sqlalchemy.Column(
                "is_active",
                sqlalchemy.Boolean(),
                server_default=sqlalchemy.sql.expression.true(),
                nullable=False,
            )