import logging
from typing import Generator

from fastapi.templating import Jinja2Templates

from db import DatabaseSession


def get_template() -> Jinja2Templates:
    """Returns jinja template for using in routes."""
    return Jinja2Templates(directory="templates")


def get_db() -> Generator[DatabaseSession, None, None]:
    """Returns database connection."""
    db = DatabaseSession()
    try:
        db.connect()
        yield db
        db.connection.commit()
    except Exception as e:
        db.connection.rollback()
        logging.error(f'Error during database operation: {e}')
        raise
    finally:
        db.close()


def get_logger() -> logging.Logger:
    """Returns logger"""
    return logging.getLogger('uvicorn.error')