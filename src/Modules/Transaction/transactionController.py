from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QMenu, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from src.Modules.Transaction.transactionUi import TransactionWindow
#from srv.Modules.Transaction.transactionService import TransactionService

class TransactionController(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = TransactionWindow()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
       