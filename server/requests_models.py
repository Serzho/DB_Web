from pydantic import BaseModel

class Auth_info(BaseModel):
    name: str
    password: str