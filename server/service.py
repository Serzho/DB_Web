from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pathlib import Path
import logging
from datetime import datetime
from fastapi.responses import JSONResponse
from sqlalchemy.ext.declarative import declarative_base

Base_auth = declarative_base()
Base_db = declarative_base()


def load_session(session_type: str) -> (Session, bool):
    db_exists = False
    engine = None
    if session_type == "auth":
        db_exists = Path.exists(Path("tmp/auth.db"))
        engine = create_engine(
            f"sqlite:///tmp/auth.db?check_same_thread=False")  # создание движка базы данных
        Base_auth.metadata.create_all(bind=engine)  # создание базы данных
    elif session_type == "data":
        db_exists = Path.exists(Path("tmp/database.db"))
        engine = create_engine(
            f"sqlite:///tmp/database.db?check_same_thread=False")  # создание движка базы данных
        Base_db.metadata.create_all(bind=engine)  # создание базы данных

    return Session(bind=engine), db_exists


def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")


def create_logger(filename: str) -> None:
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("\n" * 3 + "/" * 50)


def create_json_response(content: dict) -> JSONResponse:
    return JSONResponse(content=content)
