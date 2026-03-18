from fastapi.templating import Jinja2Templates

from db import Database

def get_template() -> Jinja2Templates:
    """ Returns jinja template for using in routes """
    return Jinja2Templates(directory="templates")

def get_db() -> Database:
    """ Returns database connection """
    return Database()
