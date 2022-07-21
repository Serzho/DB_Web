from service import load_session


class DatabaseController:
    session = None

    def __init__(self):
        self.session, __db_exists = load_session("tmp/database.db")

    def append_data(self):
        pass

    def remove_data(self):
        pass

    def select(self):
        pass
