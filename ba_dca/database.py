import sqlite3
from datetime import datetime
from typing import List, Tuple
from ba_dca.order import Order


class Database:
    """Database class to handle the app internal db."""

    def __init__(self, db_path: str) -> None:
        self._con = sqlite3.connect(db_path, check_same_thread=False)
        self._cur = self._con.cursor()
        # Create Orders table
        self._cur.execute(
            "CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "symbol TEXT, amount, freq, date)"
        )
        # Create Executed orders table
        self._cur.execute(
            "CREATE TABLE IF NOT EXISTS executed_orders(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "amount, price, date,"
            "order_id INTEGER NOT NULL, "
            "FOREIGN KEY (order_id) REFERENCES orders (id))"
        )
        self._con.commit()

    def __del__(self):
        print("Closing the database..")
        self._con.commit()
        self._cur.close()
        self._con.close()

    def _query_table(self, table_name: str, fields: str = "*") -> List[Tuple]:
        query_str = f"SELECT {fields} FROM {table_name}"
        res = self._cur.execute(query_str)
        return res.fetchall()

    def query_orders(self, fields: str = "*") -> List[Tuple]:
        """Query orders table.

        Args:
            fields (str): get specific columns (order.fields). if not passed
            the whole columns will be returned.

        Returns:
            List[Tuple]: Orders rows.
        """
        return self._query_table("orders", fields)

    def query_executed_orders(self, fields: str = "*") -> List[Tuple]:
        """Query executed orders table.

        Args:
            fields (str): get specific columns (order.fields). if not passed
            the whole columns will be returned.

        Returns:
            List[Tuple]: Orders rows.
        """
        return self._query_table("executed_orders", fields)

    def add_order(self, order: Order):
        """Add a new order to the database.

        Args:
            order (Order): New Order to be added.
        """
        order_date = order.start_date.timestamp()
        order_data = (order.symbol, order.amount, str(order.frequency), order_date)
        self._cur.execute(
            "INSERT INTO orders (symbol, amount, freq, date) VALUES(?, ?, ?, ?)",
            order_data,
        )
        self._con.commit()

    def add_executed_order(
        self, order_id: int, amount: float, price: float, date: datetime
    ):
        """Add a new order to the database.

        Args:
            order (Order): New Order to be added.
        """
        order_data = (amount, price, str(date.timestamp()), order_id)
        self._cur.execute(
            "INSERT INTO executed_orders (amount, price, date, order_id) VALUES(?, ?, ?, ?)",
            order_data,
        )
        self._con.commit()
