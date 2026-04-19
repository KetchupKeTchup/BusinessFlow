from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt

class ERMTable(QTableWidget):
    def __init__(self, columns: int, headers: list):
        super().__init__(0, columns)
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)