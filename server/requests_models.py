from pydantic import BaseModel


class Auth_request(BaseModel):  # модель запроса аутентификации
    name: str
    password: str


class Server_request(BaseModel):  # модель стандартного запроса с токеном
    command: str
    token: str


class Standard_token_request(BaseModel):  # модель стандартного запроса с токеном
    token: str


class Adding_user_token_request(BaseModel):  # модель запроса на создание нового пользователя
    token: str
    name: str
    password: str
    is_admin: str


class Deleting_user_request(BaseModel):  # модель запроса на удаление пользователя
    id: int
    token: str
