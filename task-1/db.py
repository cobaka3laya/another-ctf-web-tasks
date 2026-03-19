from functools import wraps
import logging
import sqlite3
from typing import Self

from models.product import Product


class DatabaseSession:
    """Database session class."""

    def __init__(self, db_file='db.db') -> None:
        """Database session constructor."""
        self.db_file = db_file
        self.connection = None
        
        # Initializing the products table
        self.connect()
        with self.connection.cursor() as curs:
            curs.execute('''CREATE TABLE Products 
                        (id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        image_url TEXT)''')           

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logging.error(f'Error during database connection: {e}')

    def close(self):
        """Disconnect from the SQLite database."""
        if self.connection:
            self.connection.close()

    def get_product_by_id(self, product_id: int) -> Product:
        result = None
        with self.connection.cursor() as curs:
            curs.execute(
                '''SELECT * 
                FROM Products
                WHERE id = ?
                ''',
                (product_id,)
            )
            result = curs.fetchone()

        return Product(*result)

    def add_products(self, products: list[Product]) -> None:
        """Add products to the product table."""
        for product in products:
            with self.connection.cursor() as curs:
                curs.execute(
                    '''INSERT VALUES
                    INTO Products
                    (id, name, price, image_url)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (product.id, product.name, product.price,
                    product.image_url)
                )