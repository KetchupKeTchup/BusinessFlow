from PyQt6.QtCore import QDate
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QDialog, QPushButton, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QDateEdit,  QTableWidgetItem
from PyQt6.QtCore import Qt
# from RegularPayments import RecurringPayment
from src.UI.components.erm_table import ERMTable
from src.DataBase.db_manager import RegularPaymentsDB


class RecurringPaymentWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.db = RegularPaymentsDB()
        # self.payment = RecurringPayment()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        header = QHBoxLayout()
        title = QLabel("$ Регулярні списання")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #000; color:#fff")
        # Кнопка
        self.btn_add_payment = QPushButton("+ Додати")
        self.btn_add_payment.setFixedWidth(200)
        self.btn_add_payment.clicked.connect(self.open_add_dialog)

        # Таблиця
        headers = ["Назва","Сума","Категорія","День списання"]
        self.table = ERMTable(columns=4,headers=headers)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_add_payment)
        main_layout.addLayout(header)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def open_add_dialog(self):
        new_window = NewPaymentWindow(self)

        if new_window.exec() == QDialog.DialogCode.Accepted:
            p_name = new_window.name_payment.text()
            p_sum = new_window.sum_payment.text()
            p_category = new_window.category.text()
            p_day_of_month = new_window.day_of_month.date()
            p_day_string = p_day_of_month.toString("dd.MM.yyyy")

            if not all([p_name, p_sum, p_category, p_day_of_month]):
                QMessageBox.warning(self, "Помилка", "Всі поля мають бути заповнені")
                return

            self.db.add_regula_payment(p_name,p_sum,p_category,p_day_string)
            self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        payments = self.db.get_all_regular_payments()
        for row_idx, row_data in enumerate(payments):
            self.table.insertRow(row_idx)
            # Заповнення інших колонок починаючи з індексу 1
            for col_idx in range(0, len(row_data)):
                item_text = str(row_data[col_idx])
                cell_widget = QTableWidgetItem(item_text)
                cell_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, cell_widget)


class NewPaymentWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(850, 400)

        layout_payment = QFormLayout(self)

        # Назва виплати
        self.name_payment = QLineEdit()
        # сума виплати
        self.sum_payment = QLineEdit()
        self.sum_payment.setPlaceholderText("0.00")
        validator = QDoubleValidator(0.0, 1000000.0, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.sum_payment.setValidator(validator)
        # категрія
        self.category = QLineEdit()
        # День списання
        self.day_of_month = QDateEdit()
        self.day_of_month.setCalendarPopup(True)
        self.day_of_month.setDate(QDate.currentDate())

        layout_payment.addRow("Nombre del pago",self.name_payment)
        layout_payment.addRow("Suma", self.sum_payment)
        layout_payment.addRow("Categoría", self.category)
        layout_payment.addRow("Fecha de pago", self.day_of_month)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти")
        self.btn_cancel = QPushButton("Скасувати")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        layout_payment.addRow(btn_layout)


