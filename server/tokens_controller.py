from datetime import datetime
from threading import Thread
from time import sleep
from service import base_logger


def log(message):
    module_name = "TOKENS_CONTROLLER"
    base_logger(msg=message, module_name=module_name)


class TokensController(Thread):  # контроллер созданных токенов доступа
    auth_controller = None
    is_running = False

    def __init__(self, auth_controller):
        log("Tokens controller initialized!")
        self.auth_controller = auth_controller
        Thread.__init__(self)  # инициализация родительского класса
        self.is_running = True

    def run(self):
        print("Starting tokens controller...")
        log("Starting tokens controller...")
        while self.is_running:
            sleep(15)  # задержка 15 секунд между проверками
            current_time = datetime.now()  # получение текущего времени
            tokens_list = self.auth_controller.tokens_time()
            # if len(tokens_list) > 0:
            #     print(tokens_list)  # вывод словаря с токенами
            log(f"Checking tokens: count = {len(tokens_list)}, tokens_list = {str(tokens_list)}")
            for token_dict in tokens_list:
                delta = current_time - token_dict.get("time_creation")  # разница текущего времени и времени создания
                log(f"Checking token = {token_dict.get('id')}, delta time = {delta}")
                # print(f"Delta time: {delta}")
                if delta.seconds > 300:
                    self.auth_controller.delete_token(
                        token_dict.get("id")
                    )  # удаление после 5 минут с момента создания токена
                    log(f"Token deleted! Token id = {token_dict.get('id')}, delta time = {delta}")
                    print(f"Token deleted! Id: {token_dict.get('id')}, Delta: {delta}")

        log("Token controller disabled!")
