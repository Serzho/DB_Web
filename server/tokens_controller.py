from threading import Thread
from datetime import datetime
from time import sleep
import copy

class TokensController(Thread):
    tokens_time = {}
    db_users_controller = None
    is_running = False

    def __init__(self, db_users_controller):
        self.db_users_controller = db_users_controller
        Thread.__init__(self)
        self.is_running = True

    def run(self):
        print("Starting tokens controller... %d" % self.is_running)
        while self.is_running:
            sleep(15)
            current_time = datetime.now()
            print(self.tokens_time)
            for id_token in self.tokens_time:
                delta = current_time - self.tokens_time.get(id_token)
                print(f"Delta time: {delta}")
                if delta.seconds > 300:
                    self.db_users_controller.delete_token(id_token)
                    print(f"Token deleted! Id: {id_token}, Delta: {delta.seconds}")

        self.db_users_controller.clear_access_tokens()
        print("Stopped tokens controller!!!")