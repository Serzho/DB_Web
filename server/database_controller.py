import sqlite3
from datetime import datetime

import sqlalchemy.exc

from service import load_session, base_logger
from data_table import Data


def log(msg: str) -> None:
    module_name = "DATABASE CONTROLLER"
    base_logger(msg=msg, module_name=module_name)


class DatabaseController:
    session = None

    def __init__(self):
        self.session, __db_exists = load_session("data")
        log("Database controller initialized!")

    def append_data(self, author_id: int, key: str, value: str) -> None:
        current_date = datetime.now()
        log(f"Appending data: author_id = {author_id}, key = {key}, value = {value}, time_creation = {current_date}")
        data_row = Data(author_id=author_id, key=key, value=value, time_creation=current_date)
        self.session.add(data_row)
        self.session.commit()
        log("Data row was successfully added!")

    def remove_data(self, id_row: int) -> bool:
        log(f"Removing data row with id = {id_row}")
        data_row = self.session.query(Data).filter(Data.id == id_row).first()
        if data_row is not None:
            self.session.delete(data_row)
            self.session.commit()
            log(f"Data row with id = {id_row} was successfully removed!")
            return True
        else:
            log(f"Data row with id = {id_row} wasn't find!")
            return False

    def select(self, sql_request: str) -> (bool, list):
        log(f"Selecting data by request = {sql_request}")
        returning_list = []
        try:
            sql_response = self.session.execute(sql_request)
            for row in sql_response:
                returning_list.append(list(row))
            log(f"Successful selecting request!")
            return True, returning_list
        except (sqlalchemy.exc.OperationalError, sqlite3.OperationalError):
            log("Bad sql request!")
            return False, returning_list

