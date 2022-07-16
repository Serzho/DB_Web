from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pathlib import Path
import logging
from datetime import datetime
from fastapi.responses import JSONResponse
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def load_session() -> (Session, bool):
    db_exists = Path.exists(Path("tmp/database.db"))
    engine = create_engine(
        "sqlite:///tmp/database.db?check_same_thread=False")  # создание движка базы данных
    Base.metadata.create_all(engine)  # создание базы данных
    return Session(bind=engine), db_exists


def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")


def create_logger(filename: str) -> None:
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("\n" * 3 + "/" * 50)


def create_json_response(content: dict) -> JSONResponse:
    return JSONResponse(content=content)
