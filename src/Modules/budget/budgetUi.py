from PyQt6.QtCore import QDate
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QDialog, QPushButton, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QDateEdit,  QTableWidgetItem
from PyQt6.QtCore import Qt
# from RegularPayments import RecurringPayment
from src.UI.components.erm_table import ERMTable



class BudgetWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        header = QHBoxLayout()
        title = QLabel("$ Планування бюджету")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #000; color:#fff")
        # Кнопка
        self.btn_add_payment = QPushButton("+ Додати")
        self.btn_add_payment.setFixedWidth(200)
        # self.btn_add_payment.clicked.connect(self.open_add_dialog)

        # Таблиця
        headers = ["Назва","Сума","Категорія","День списання"]
        self.table = ERMTable(columns=4,headers=headers)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_add_payment)
        main_layout.addLayout(header)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)