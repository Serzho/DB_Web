from datetime import datetime
from threading import Thread
from time import sleep


class TokensController(Thread):  # контроллер созданных токенов доступа
    tokens_time = {}  # словарь {id пользователя с открытым токеном: время создания токена}
    db_users_controller = None
    is_running = False

    def __init__(self, db_users_controller):
        self.db_users_controller = db_users_controller
        Thread.__init__(self)  # инициализация родительского класса
        self.is_running = True

    def run(self):
        print("Starting tokens controller... %d" % self.is_running)
        while self.is_running:
            sleep(15)  # задержка 15 секунд между проверками
            current_time = datetime.now()  # получение текущего времени
            print(self.tokens_time)  # вывод словаря с токенами
            for id_token in self.tokens_time:
                delta = current_time - self.tokens_time.get(id_token)  # разница текущего времени и времени создания
                print(f"Delta time: {delta}")
                if delta.seconds > 300:
                    self.db_users_controller.delete_token(id_token)  # удаление после 5 минут с момента создания токена
                    print(f"Token deleted! Id: {id_token}, Delta: {delta.seconds}")

        self.db_users_controller.clear_access_tokens()  # очистка всех токенов при выходе
        print("Stopped tokens controller!!!")
