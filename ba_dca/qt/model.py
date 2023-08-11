from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class OrdersModel:
    def __init__(self):
        self.model = self._create_model()

    @staticmethod
    def _create_model():
        """Create and set up the model."""
        table_model = QSqlTableModel()
        table_model.setTable("orders")
        table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        table_model.select()
        headers = ("Symbol", "Amount", "Frequency", "Date")
        for column_index, header in enumerate(headers):
            table_model.setHeaderData(column_index, Qt.Horizontal, header)

        return table_model
