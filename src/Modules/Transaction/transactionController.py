from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QMenu, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from src.Modules.Transaction.transactionUi import TransactionWindow, AddTransactionDialog
from src.Modules.Transaction.transactionService import TransactionService

class TransactionController(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = TransactionWindow()
        self.service = TransactionService()
        self.connect_signals()
        self.load_data()  # Завантажуємо дані при ініціалізації

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 0)
        layout.addWidget(self.ui)

    def connect_signals(self):
        # Підключення сигналів для кнопок та інших елементів
        self.ui.btn_add.clicked.connect(self.open_add_new_transaction)
        # self.ui.table.customContextMenuRequested.connect(self.show_context_menu)
       
    def open_add_new_transaction(self):
        """Відкриває діалогове вікно"""
        dialog =  AddTransactionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Витягуємо дані з полів вікна
            t_type = dialog.type_combo.currentText()
            t_category = dialog.category_input.text()
            raw_sum_text = dialog.sum_input.text()

            if not raw_sum_text:
                QMessageBox.warning(self, "Помилка", "Сума не може бути порожньою!")
                return
            #Замінюємо кому на крапку якщо користувач не то ввів
            t_sum = float(raw_sum_text.replace(",", "."))
            if t_sum <= 0:
                QMessageBox.warning(self, "Помилка", "Сума повинна бути більшою за нуль!")
                return

            # Записуємо в базу
            self.service.add_transaction(trans_type=t_type, category=t_category, amount=t_sum)

            # Оновлюємо таблицю, щоб побачити новий запис
            self.load_data()
        
    def load_data(self):
        """Координує оновлення таблиці"""
        # 1. Просимо Сервіс дати нам дані
        data = self.service.load_data()
        
        # (Тут Контролер міг би якось додатково відфільтрувати data, якщо треба)
        
        # 2. Віддаємо ці дані в UI для відмальовування
        self.ui.fill_table(data)