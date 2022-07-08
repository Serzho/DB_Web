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
    return True


@app.get("/item")  #
async def get_item():
    # print("ANSWER")
    return FileResponse("tmp/database.db")


@app.post("/auth")  # запрос аутентификации
async def auth(auth_info: Auth_info):
    # print(auth_info.name, auth_info.password)
    id_user, token = db_users_controller.auth_user(auth_info.name, auth_info.password)
    if id_user == -1:
        return ""
    else:
        return token

@app.get("/test_token")
async def test_token(test_token: Standart_token_request):
    print(f"Testing token {test_token.token}")
    result = db_users_controller.check_token_exists(test_token.token)
    if result:
        print("Correct access token!")
    else:
        print("Incorrect access token!")
    return result

@app.get("/get_users")
async def get_users(token_request: Standart_token_request):
    if db_users_controller.check_token_exists(token_request.token) and db_users_controller.check_token_admin(token_request.token):
        return db_users_controller.get_users_dict()
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        return None

@app.get("/add_user")
async def get_users(token_request: Adding_user_token_request):
    if db_users_controller.check_token_exists(token_request.token) and db_users_controller.check_token_admin(token_request.token):
        db_users_controller.add_user( id= db_users_controller.next_user_id(), name= token_request.name, password= token_request.password, is_admin=token_request.is_admin == "True")
        return "Correct creation!"
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        return f"Admin request with incorrect token!!! Token: {token_request.token}"

"""@app.middleware("http")  
async def debug_request(request: Request, call_next):
    response = await call_next(request)
    print(Request.base_url)
    return response"""

uvicorn.run(app=app, host="localhost", port=9999)  # запуск сервера
db_users_controller.stop_tokens_controller()
