# -*- coding: utf-8 -*-

"""This module provides views to manage the orders table."""
import sys
import os
import pathlib
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QApplication,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from ba_dca.qt.model import OrdersModel
from ba_dca.qt.database import create_connection

here = pathlib.Path(__file__).parent.resolve()


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # uic.loadUi(str(here) + "/main.ui", self)  # Load the .ui file
        self.setWindowTitle("Binance DCA")
        self.resize(678, 678)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.layout.sizeHint
        self.centralWidget.setLayout(self.layout)
        self.orders_model = OrdersModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""

        # Create the table view widget
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.setModel(self.orders_model.model)
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.deleteButton = QPushButton("Delete")
        self.clearAllButton = QPushButton("Clear All")
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)


def enable_dark_theme(app: QApplication):
    """Enable dark theme color palette.

    Args:
        app (QApplication): Qt application.
    """
    app.setStyle("Fusion")
    # # Now use a palette to switch to dark colors:
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    app.setPalette(dark_palette)


def main():
    """Binance DCA main function."""
    # Create the application
    app = QApplication(sys.argv)
    enable_dark_theme(app)
    # Create and connect db
    home = os.environ["HOME"]
    database_path = os.path.join(home, ".ba_dca/ba_dca.db")
    if not os.path.exists(home + "/.ba_dca"):
        os.mkdir(home + "/.ba_dca")
    create_connection(database_path)
    # Create the main window
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())
