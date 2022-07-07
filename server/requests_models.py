from pydantic import BaseModel


class Auth_info(BaseModel):  # модель запроса аутентификации
    name: str
    password: str
