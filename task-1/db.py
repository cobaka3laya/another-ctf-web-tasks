from functools import wraps
import sqlite3
import logging

from models.product import Product

def cursor_connection(func):
    """ Decorator for automatic database connection and disconnection """
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('db.db')
        try:
            kwargs["cursor"] = conn.cursor
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            logging.error(f'Database error: {e}')
            raise
        finally:
            conn.commit()
            conn.close()
    return wrapper


class Database:
    @cursor_connection
    def __init__(self, cursor=None) -> None:
        ''' Init the database '''
        if not cursor:
            return

        with cursor() as _cursor:
            _cursor.execute('''CREATE TABLE Products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL, image_url TEXT)''')
    
    @staticmethod
    def insert_products(products: list[Product], cursor=None) -> None:
        ''' Insert products into the database '''
        if not cursor:
            return

        with cursor() as _cursor:
            for product in products:
                _cursor.execute(
                    '''INSERT VALUES INTO Products (id, name, price, image_url) VALUES (?, ?, ?, ?)''', 
                    (product.id, product.name, product.price, product.image_url)
                )

    @staticmethod
    def get_product_by_id(id: int, cursor=None) -> Product:
        ''' Get products from database by ID '''
        if not cursor:
            return
        
        result = None
        with cursor() as _cursor:
            _cursor.execute(
                '''SELECT * FROM Products WHERE id = ?''',
                (id,)
            )
            result = _cursor.fetchone()

        return Product(*result)


    