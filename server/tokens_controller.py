from datetime import datetime
from threading import Thread
from time import sleep


class TokensController(Thread):  # контроллер созданных токенов доступа
    db_users_controller = None
    is_running = False

    def __init__(self, db_users_controller):
        self.db_users_controller = db_users_controller
        Thread.__init__(self)  # инициализация родительского класса
        self.is_running = True

    def run(self):
        print("Starting tokens controller...")
        while self.is_running:
            sleep(15)  # задержка 15 секунд между проверками
            current_time = datetime.now().time()  # получение текущего времени
            seconds_current_time = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
            tokens_list = self.db_users_controller.get_tokens()
            if len(tokens_list) > 0:
                print(tokens_list)  # вывод словаря с токенами
            for token_dict in tokens_list:
                delta = seconds_current_time - token_dict.get("time_creation")  # разница текущего времени и времени создания
                # print(f"Delta time: {delta}")
                if delta > 300:
                    self.db_users_controller.delete_token(token_dict.get("id"))  # удаление после 5 минут с момента создания токена
                    print(f"Token deleted! Id: {token_dict.get('id')}, Delta: {delta}")

        self.db_users_controller.clear_access_tokens()  # очистка всех токенов при выходе
