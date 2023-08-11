from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def _create_orders_table():
    """Create the contacts table in the database."""
    create_table_query = QSqlQuery()
    return create_table_query.exec(
        """
        CREATE TABLE IF NOT EXISTS orders (
            symbol VARCHAR(40) NOT NULL,
            amount REAL,
            freq TEXT,
            date TEXT
        )
        """
    )


def create_connection(database_name: str) -> bool:
    """Create a new Qt database connection.

    Args:
        databaseName (str): Database name.

    Returns:
        bool: True if connected, False otherwise.
    """
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(database_name)
    if not connection.open():
        QMessageBox.warning(
            None,
            "RP Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    _create_orders_table()
    return True
