from db_users_controller import DB_Users_Controller
from fastapi import *
from fastapi.responses import FileResponse
import uvicorn
from requests_models import *


print("Starting_server...")
db_users_controller = DB_Users_Controller()  # инициализация контроллеа базы данных пользователей
app = FastAPI()  # создание приложения fast_api


@app.get("/test")  # вывод сообщения при тестовом запросе
async def test():
    print("TEST")
    return "Successfully connect to server!"


@app.get("/item")  #
async def get_item():
    # print("ANSWER")
    return FileResponse("tmp/database.db")


@app.post("/auth")  # запрос аутентификации
async def auth(auth_info: Auth_info):
    # print(auth_info.name, auth_info.password)
    id_user, token = db_users_controller.auth_user(auth_info.name, auth_info.password)
    if id_user == -1:
        return "Incorrect name or password"
    else:
        return f"Correct authentication! Name: {auth_info.name}, Token: {token}"


"""@app.middleware("http")  
async def debug_request(request: Request, call_next):
    response = await call_next(request)
    print(Request.base_url)
    return response"""

uvicorn.run(app=app, host="localhost", port=9999)  # запуск сервера
db_users_controller.stop_tokens_controller()
