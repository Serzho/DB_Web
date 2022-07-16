from db_users_controller import DBUsersController
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from requests_models import *
from user_table import NAME_MAX_LENGTH
from service import base_logger, create_logger, create_json_response

# главный исполняемый файл сервера

create_logger("server.log")


def log(message):
    module_name = "SERVER"
    base_logger(msg=message, module_name=module_name)


log("Starting_server...")
print("Starting_server...")
db_users_controller = DBUsersController()  # инициализация контроллера базы данных пользователей
app = FastAPI()  # создание приложения fast_api
log("App created!")


@app.get("/test")  # тестовый запрос наличия запущенного сервера
async def test() -> JSONResponse:
    # print("TEST")
    log("Test request")
    return create_json_response({"success": 1})


@app.get("/item")  # получение файла базы данных пользователей
async def get_item() -> FileResponse:
    # print("ANSWER")
    log("Database file request")
    return FileResponse("tmp/database.db")


@app.get("/auth")  # запрос аутентификации
async def auth(auth_info: Auth_request) -> JSONResponse:
    # print(auth_info.name, auth_info.password)
    # получение токена и id пользователя
    log(f"Auth request with name: {auth_info.name}, password: {auth_info.password}")
    id_user, token = db_users_controller.auth_user(auth_info.name, auth_info.password)
    log(f"Result: success = {token is not None}, token = {token}")
    print(f"Returning token {token}")
    return create_json_response({"success": token is not None, "data": token})


@app.get("/test_token")  # запрос проверки токена
async def test_token(token_request: Standard_token_request) -> JSONResponse:
    print(f"Testing token {token_request.token}")
    log(f"Testing token request: token = {token_request.token}")
    result = db_users_controller.token_exists(token_request.token)  # проверка существования токена
    log(f"Result: success = {result}")
    return create_json_response({"success": result})


@app.get("/get_users")  # запрос получения списка словарей с данными пользователей
async def get_users(token_request: Standard_token_request) -> JSONResponse:
    # проверка токена и прав доступа админа для совершения запроса
    log(f"Getting users request: token = {token_request.token}")
    if db_users_controller.token_exists(token_request.token) and db_users_controller.token_is_admin(
            token_request.token) and token_request.token != "":
        log(f"Result: success = {True}, len of users list = {len(db_users_controller.users_list())}")
        return create_json_response({"success": True, "data": db_users_controller.users_list()})
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        print(f"Token exists: {db_users_controller.token_exists(token_request.token)}")
        print(f"Admin rights: {db_users_controller.token_is_admin(token_request.token)}")
        log(f"Result: success = {False}, "
            f"token exists = {db_users_controller.token_exists(token_request.token)}, "
            f"having admin rights = {db_users_controller.token_is_admin(token_request.token)}")
        return create_json_response({"success": False})


@app.get("/add_user")  # запрос добавления нового пользователя
async def add_user(token_request: Adding_user_token_request) -> JSONResponse:
    # проверка токена и прав доступа админа для совершения запроса
    log(f"Adding user request: token = {token_request.token}, "
        f"name = {token_request.name}, "
        f"password = {token_request.password}, "
        f"is_admin = {token_request.is_admin}")
    if db_users_controller.token_exists(token_request.token) and db_users_controller.token_is_admin(
            token_request.token):
        # вызов функции добавления нового пользователя
        print(len(token_request.name))
        if len(token_request.name) > NAME_MAX_LENGTH:
            log(f"Result: success = {False}, Incorrect name length!")
            return create_json_response({"success": False, "data": "Incorrect name length (more than 100 characters)"})
        db_users_controller.add_user(name=token_request.name,
                                     password=token_request.password, is_admin=token_request.is_admin == "True")
        log(f"Result: success = {True}, Correct creation!")
        return create_json_response({"success": True, "data": "Correct creation!"})
    else:
        print(f"Admin request with incorrect token!!! Token: {token_request.token}")
        log(f"Result: success = {False}, Incorrect token to admin request")
        return create_json_response(
            {"success": False, "data": f"Admin request with incorrect token!!! Token: {token_request.token}"}
        )


@app.get("/log_out")  # запрос отключения токена (выхода из учетной записи)
async def log_out(token_request: Standard_token_request):
    # получение id токена и удаление его
    log(f"Logged out request, token = {token_request.token}")
    db_users_controller.delete_token(db_users_controller.get_token_id(token_request.token))


@app.get("/delete_user")  # запрос удаления пользователя
async def delete_user(token_request: Deleting_user_request) -> JSONResponse:
    # проверка токена и прав администратора
    log(f"Deleting user request, token = {token_request.token}, id of deleting user = {token_request.id}")
    if db_users_controller.token_exists(token_request.token) and db_users_controller.token_is_admin(
            token_request.token):
        db_users_controller.delete_user(token_request.id)  # вызов функции удаления пользователя
        log(f"Result: success = {True}, Correct deleting user")
        return create_json_response({"success": True, "data": f"Correct deleting user with id = {token_request.id}!"})
    else:
        log(f"Result: success = {False}, Incorrect token to admin request")
        return create_json_response(
            {"success": False, "data": f"Admin request with incorrect token!!! Token: {token_request.token}"}
        )


"""@app.middleware("http")  
async def debug_request(request: Request, call_next):
    response = await call_next(request)
    print(Request.base_url)
    return response"""

uvicorn.run(app=app, host="localhost", port=9999)  # запуск сервера
log(f"Stopping server...")
db_users_controller.stop_tokens_controller()  # остановка потока с контроллером токенов после остановки сервера
