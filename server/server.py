from db_users_controller import DbUsersController
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from requests_models import *
from db_users_create import NAME_MAX_LENGTH

# главный исполняемый файл сервера

print("Starting_server...")
db_users_controller = DbUsersController()  # инициализация контроллера базы данных пользователей
app = FastAPI()  # создание приложения fast_api


@app.get("/test")  # тестовый запрос наличия запущенного сервера
async def test() -> JSONResponse:
    print("TEST")
    return JSONResponse(content={"success": 1})


@app.get("/item")  # получение файла базы данных пользователей
async def get_item() -> FileResponse:
    # print("ANSWER")
    return FileResponse("tmp/database.db")


@app.get("/auth")  # запрос аутентификации
async def auth(auth_info: Auth_request) -> JSONResponse:
    # print(auth_info.name, auth_info.password)
    # получение токена и id пользователя
    id_user, token = db_users_controller.auth_user(auth_info.name, auth_info.password)
    print(f"Returning token {token}")
    return JSONResponse(content={"success": token is not None, "data": token})


@app.get("/test_token")  # запрос проверки токена
async def test_token(token_request: Standard_token_request) -> JSONResponse:
    print(f"Testing token {token_request.token}")
    result = db_users_controller.check_token_exists(token_request.token)  # проверка существования токена
    return JSONResponse(content={"success": result})


@app.get("/get_users")  # запрос получения списка словарей с данными пользователей
async def get_users(token_request: Standard_token_request) -> JSONResponse:
    # проверка токена и прав доступа админа для совершения запроса
    if db_users_controller.check_token_exists(token_request.token) and db_users_controller.check_token_admin(
            token_request.token) and token_request.token != "":
        return JSONResponse(content={"success": True, "data": db_users_controller.get_users_list()})
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        print(f"Token exists: {db_users_controller.check_token_exists(token_request.token)}")
        print(f"Admin rights: {db_users_controller.check_token_admin(token_request.token)}")
        return JSONResponse(content={"success": False})


@app.get("/add_user")  # запрос добавления нового пользователя
async def add_user(token_request: Adding_user_token_request) -> JSONResponse:
    # проверка токена и прав доступа админа для совершения запроса
    if db_users_controller.check_token_exists(token_request.token) and db_users_controller.check_token_admin(
            token_request.token):
        # вызов функции добавления нового пользователя
        print(len(token_request.name))
        if len(token_request.name) > NAME_MAX_LENGTH:
            return JSONResponse(content={"success": False, "data": "Incorrect name length (more than 100 characters)"})
        db_users_controller.add_user(name=token_request.name,
                                     password=token_request.password, is_admin=token_request.is_admin == "True")
        return JSONResponse(content={"success": True, "data": "Correct creation!"})
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        return JSONResponse(
            content={"success": False, "data": f"Admin request with incorrect token!!! Token: {token_request.token}"})


@app.get("/log_out")  # запрос отключения токена (выхода из учетной записи)
async def log_out(token_request: Standard_token_request):
    # получение id токена и удаление его
    db_users_controller.delete_token(db_users_controller.get_token_id(token_request.token))


@app.get("/delete_user")  # запрос удаления пользователя
async def delete_user(token_request: Deleting_user_request) -> JSONResponse:
    # проверка токена и прав администратора
    if db_users_controller.check_token_exists(token_request.token) and db_users_controller.check_token_admin(
            token_request.token):
        db_users_controller.delete_user(token_request.id)  # вызов функции удаления пользователя
        return JSONResponse(content={"success": True, "data": f"Correct deleting user with id = {token_request.id}!"})
    else:
        return JSONResponse(
            content={"success": False, "data": f"Admin request with incorrect token!!! Token: {token_request.token}"})


"""@app.middleware("http")  
async def debug_request(request: Request, call_next):
    response = await call_next(request)
    print(Request.base_url)
    return response"""

uvicorn.run(app=app, host="localhost", port=9999)  # запуск сервера
db_users_controller.stop_tokens_controller()  # остановка потока с контроллером токенов после остановки сервера
