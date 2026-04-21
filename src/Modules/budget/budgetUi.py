from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTableWidgetItem
from PyQt6.QtCore import Qt
from src.UI.components.erm_table import ERMTable


class BudgetWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        header = QHBoxLayout()
        title = QLabel("$ Планування бюджету")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color:#fff")

        # Кнопка
        self.btn_add_payment = QPushButton("+ Додати")
        self.btn_add_payment.setFixedWidth(200)

        # Таблиця
        headers = ["Categoría", "Previsto (2026)", "Gastado", "Resto"]
        self.table = ERMTable(columns=4, headers=headers)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_add_payment)
        main_layout.addLayout(header)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def fill_table(self, data_list):
        """Цей метод просто бере список і заповнює таблицю"""
        if not data_list:
            return

        # self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data_list):
            self.table.insertRow(row_idx)

            # Очікуємо 3 параметри: назва, план, факт
            name, planned, spent = row_data
            remaining = planned - spent

            name_item = QTableWidgetItem(str(name))
            plan_item = QTableWidgetItem(f"{planned:,.2f} €")
            spent_item = QTableWidgetItem(f"{spent:,.2f} €")
            rem_item = QTableWidgetItem(f"{remaining:,.2f} €")

            for item in [plan_item, spent_item, rem_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            if remaining < 0:
                rem_item.setForeground(Qt.GlobalColor.red)

            self.table.setItem(row_idx, 0, name_item)
            self.table.setItem(row_idx, 1, plan_item)
            self.table.setItem(row_idx, 2, spent_item)
            self.table.setItem(row_idx, 3, rem_item)