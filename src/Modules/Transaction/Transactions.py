from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QComboBox,
                             QDoubleSpinBox, QMessageBox, QTableWidgetItem,QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from src.DataBase.db_manager import TransactionManager

class AddTransactionDialog(QDialog):
    """Спливаюче вікно для додавання нової транзакції"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати транзакцію")
        self.setFixedSize(850,400)

        layout = QFormLayout(self)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Витрати", "Дохід", "Підписка","Регулярний платіж"])

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Наприклад: Продукти, Авто...")

        self.sum_input = QLineEdit()
        self.sum_input.setPlaceholderText("0.00")
        # Валідатор від 0.0 до 100000, максимум 2 знаки після коми
        validator = QDoubleValidator(0.0, 1000000.0, 2)
        # StandardNotation гарантує, що не буде експонеційного формату(типу 1е+06)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.sum_input.setValidator(validator)


        #Кнопки
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти")
        self.btn_cancel = QPushButton("Скасувати")

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addRow("Тип", self.type_combo)
        layout.addRow("Категорія", self.category_input)
        layout.addRow("Сума", self.sum_input)
        layout.addRow(btn_layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)


class Transactions(QWidget):
    def __init__(self):
        super().__init__()
        self.db = TransactionManager()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Головний layout для цього екрану
        layout = QVBoxLayout(self)
        layout.setObjectName("layout")

        # Верхня панель (Заголовок і кнопка додавання)
        top_panel = QHBoxLayout()

        title = QLabel("💳 Транзакції")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #000; color:#fff")

        self.btn_add = QPushButton("+ Нова транзакція")
        self.btn_add.setFixedWidth(200)
        self.btn_add.clicked.connect(self.open_add_dialog)

        top_panel.addWidget(title)
        top_panel.addStretch()  # Відштовхує кнопку вправо
        top_panel.addWidget(self.btn_add)

        # Таблиця
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Номер", "Дата", "Тип", "Категорія", "Сума", "Статус"])
        # self.table.setColumnWidth(6,160)

        # Робимо так, щоб колонки автоматично розтягувалися на всю ширину
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Дозвіл на кастомне контекстн меню
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # Підключення сигнала правого натискання мишки
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.verticalHeader().setVisible(False)

        # Додаємо все на головний екран модуля
        layout.addLayout(top_panel)
        layout.addWidget(self.table)

    def open_add_dialog(self):
        """Відкриває вікно додавання та обробляє результат"""
        dialog = AddTransactionDialog(self)

        # Якщо користувач натиснув "Зберегти" (accept)
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
            self.db.add_transaction(trans_type=t_type, category=t_category, amount=t_sum)

            # Оновлюємо таблицю, щоб побачити новий запис
            self.load_data()

    def load_data(self):
        """Очищає таблицю і заповнює її даними з бази"""
        self.table.setRowCount(0)  # Очищення старих рядків
        transactions = self.db.get_all_transactions() # отримання всіх даних

        for row_idx, row_data in enumerate(transactions):
            self.table.insertRow(row_idx)
            real_db_id = row_data[0]

            # Колонка 0: Створення візуального порядкового номеру
            visual_number = str(row_idx + 1)
            cell_id_widget = QTableWidgetItem(visual_number)
            cell_id_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Приховування справжнього id всередині цієї клітинки (UserRole - це сховище для розробника)
            cell_id_widget.setData(Qt.ItemDataRole.UserRole, real_db_id)
            self.table.setItem(row_idx, 0, cell_id_widget)

            # Заповнення інших колонок починаючи з індексу 1
            for col_idx in range(1, len(row_data)):
                item_text = str(row_data[col_idx])
                cell_widget = QTableWidgetItem(item_text)
                cell_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, cell_widget)

    def show_context_menu(self, position):
        """Create and show context menu"""
        # Отримуємо індекс рядка по якому клікнули
        row_table = self.table.rowAt(position.y())
        if row_table < 0:
            return
        # виділяємо весь рядок
        self.table.selectRow(row_table)

        # Створення меню
        menu = QMenu()

        # Додаємо дії
        edit_action = menu.addAction("Редагувати")
        delete_action = menu.addAction("Видалити")

        # Показує меню там, де находиться курсок миші
        action = menu.exec(self.table.viewport().mapToGlobal(position))

        # Обробка вибора користувача
        if action == edit_action:
            self.edit_record(row_table)
        elif action == delete_action:
            self.delete_record(row_table)

    def delete_record(self, row_table):
        """Logic for deleting record"""

        # Витягуємо id транзакції з першої колонки (індекс 0)
        t_id_item = self.table.item(row_table, 0)
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
            self.db.delete_transaction(t_id)
            # оновлення
            self.load_data()

    def edit_record(self, row_table):
        """Logic for editing record"""
        t_id = self.table.item(row, 0).text()
        t_sum = self.table.item(row, 4).text()

        QMessageBox.information(
            self,
            "Редагування",
            f"Тут буде відкриватися модальне вікно для редагування запису #{t_id}.\nПоточна сума: {t_sum}"
        )















