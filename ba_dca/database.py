import sqlite3
from typing import List, Tuple
from ba_dca.order import Order
from ba_dca.frequency import Frequency, relativedelta

class Database:
    """Database class to handle the app internal db."""

    def __init__(self, db_path: str) -> None:
        self._con = sqlite3.connect(db_path)
        self._cur = self._con.cursor()
        self._cur.execute(
            "CREATE TABLE IF NOT EXISTS orders(symbol TEXT, amount, freq, date)"
        )
        self._con.commit()

    def __del__(self):
        print("Closing the database..")
        self._con.commit()
        self._cur.close()
        self._con.close()

    def query_orders(self, fields: str = "*") -> List[Tuple]:
        """Query orders table.

        Args:
            fields (str): get specific columns (order.fields). if not passed
            the whole columns will be returned.

        Returns:
            List[Tuple]: Orders rows.
        """
        query_str = f"SELECT {fields} FROM orders"
        res = self._cur.execute(query_str)
        return res.fetchall()

    def add_order(self, order: Order):
        """Add a new order to the database.

        Args:
            order (Order): New Order to be added.
        """
        order_date = order.start_date.timestamp()
        order_data = (order.symbol, order.amount, str(order.frequency), order_date)
        self._cur.execute("INSERT INTO orders VALUES(?, ?, ?, ?)", order_data)
        self._con.commit()
