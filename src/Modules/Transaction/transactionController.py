from PyQt6.QtWidgets import QHeaderView, QMessageBox, QTableWidgetItem, QDialog, QMenu, QWidget, QVBoxLayout
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
        
        # Дозвіл на кастомне контекстн меню
        self.ui.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Підключення сигнала правого натискання мишки
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)

       
    def open_add_new_transaction(self):
        """Відкриває діалогове вікно"""
        dialog =  AddTransactionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            
            t_type = dialog.type_combo.currentText()
            t_category = dialog.category_input.text()
            raw_sum_text = dialog.sum_input.text()

            if not raw_sum_text:
                QMessageBox.warning(self, "Помилка", "Сума не може бути порожньою!")
                return
            t_sum = float(raw_sum_text.replace(",", "."))
            if t_sum <= 0:
                QMessageBox.warning(self, "Помилка", "Сума повинна бути більшою за нуль!")
                return
            
            self.service.add_transaction(trans_type=t_type, category=t_category, amount=t_sum)
            self.load_data()
        
    def load_data(self):
        """Координує оновлення таблиці"""
        data = self.service.load_data()
        self.ui.fill_table(data)

    def show_context_menu(self, position):
        """Create and show context menu"""
        # Отримуємо індекс рядка по якому клікнули
        row_table = self.ui.table.rowAt(position.y())
        if row_table < 0:
            return
        # виділяємо весь рядок
        self.ui.table.selectRow(row_table)

        # Створення меню
        menu = QMenu()

        # Додаємо дії
        edit_action = menu.addAction("Редагувати")
        delete_action = menu.addAction("Видалити")

        # Показує меню там, де находиться курсок миші
        action = menu.exec(self.ui.table.viewport().mapToGlobal(position))

        # Обробка вибора користувача
        if action == edit_action:
            self.edit_record(row_table)
        elif action == delete_action:
            self.delete_record(row_table)

    def delete_record(self, row_table):

        """Logic for deleting record"""

        # Витягуємо id транзакції з першої колонки (індекс 0)
        t_id_item = self.ui.table.item(row_table, 0)
        if not t_id_item:
            return
        # Дістаємо справжній ід з бази даних замість візуального тексту
        t_id = t_id_item.data(Qt.ItemDataRole.UserRole)

        # Підтвердження користувача
        reply = QMessageBox.question(
            self,
            "Підтвердження",
            f"Ви впевнені, що хочите видалити запис №{t_id}?",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_transaction(t_id)
            # оновлення
            self.load_data()

    def edit_record(self, row_table):
        """Logic for editing record"""
        t_id = self.ui.table.item(row_table, 0).text()
        t_sum = self.ui.table.item(row_table, 4).text()

        QMessageBox.information(
            self,
            "Редагування",
            f"Тут буде відкриватися модальне вікно для редагування запису #{t_id}.\nПоточна сума: {t_sum}"
        )




