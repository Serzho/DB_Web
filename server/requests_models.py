from pydantic import BaseModel


class Auth_info(BaseModel):  # модель запроса аутентификации
    name: str
    password: str

class Server_request(BaseModel):  # модель стандартного запроса с токеном
    command: str
    token: str

class Standart_token_request(BaseModel): # модель запроса с токеном
    token: str

class Adding_user_token_request(BaseModel):
    token: str
    name: str
    password: str
    is_admin: str
