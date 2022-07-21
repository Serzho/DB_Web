from datetime import datetime

from service import load_session
from data_table import Data


class DatabaseController:
    session = None

    def __init__(self):
        self.session, __db_exists = load_session("data")

    def append_data(self, author_id: int, key: str, value: str) -> None:
        print(author_id, key, value)
        current_date = datetime.now()
        data_row = Data(author_id=author_id, key=key, value=value, time_creation=current_date)
        self.session.add(data_row)
        self.session.commit()

    def remove_data(self, id_row: int) -> bool:
        data_row = self.session.query(Data).filter(Data.id == id_row).first()
        if data_row is not None:
            self.session.delete(data_row)
            self.session.commit()
            return True
        else:
            return False

    def select(self, sql_request: str):
        sql_response = self.session.execute(sql_request)
        returning_list = []
        for row in sql_response:
            returning_list.append(list(row))
        return returning_list

