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
        self._init_tables_()

    def _init_tables_(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Products 
                    (id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    image_url TEXT)''')           
        self.connection.commit()

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logging.error(f'Error during database connection: {e}')

    def close(self):
        """Disconnect from the SQLite database."""
        if self.connection:
            self.connection.close()

    def get_product_by_id(self, product_id: int) -> Product:
        result = None
        self.cursor.execute(
            '''SELECT * 
            FROM Products
            WHERE id = ?
            ''',
            (product_id,)
        )

        result = self.cursor.fetchone()

        return Product(*result)

    def get_products(self, offset, limit) -> list[Product]:
        results = []
        self.cursor.execute(
            '''SELECT *
            FROM Products
            ORDER BY id
            LIMIT ?
            OFFSET ?
            ''',
            (limit, offset)
        )

        results = self.cursor.fetchall()

        return [Product(*result) for result in results]

    def add_products(self, products: list[Product]) -> None:
        """Add products to the product table."""
        for product in products:
            self.cursor.execute(
                '''INSERT OR REPLACE
                INTO Products
                (id, name, price, image_url)
                VALUES (?, ?, ?, ?)
                ''',
                (product.id, product.name, product.price,
                product.image_url)
            )
            self.connection.commit()
