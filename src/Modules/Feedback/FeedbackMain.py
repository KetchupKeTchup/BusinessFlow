from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit,
    QMessageBox, QMenu, QTableWidgetItem, QLineEdit
)
from PyQt6.QtCore import Qt
from src.DataBase.db_manager import FeedbackManager

class AddFeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Додати нову Скаргу або Пропозицію")
        self.setFixedSize(850,600)

        form_layout = QFormLayout(self)
        self.option = QComboBox()
        self.option.addItems(["Скарга", "Пропозиція"])

        self.author_name = QLineEdit()
        self.author_name.setPlaceholderText("Вкажіть ім'я.")

        self.priority = QComboBox()
        self.priority.addItems(["Високий", "Середній", "Низький"])

        self.text_feedback = QTextEdit()

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Додати")
        self.btn_cancel = QPushButton("Скасувати")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_cancel)

        form_layout.addRow("Вибір", self.option)
        form_layout.addRow("Ім'я хто запропонував", self.author_name)
        form_layout.addRow("Важливість", self.priority)
        form_layout.addRow("Опис", self.text_feedback)
        form_layout.addRow(btn_layout)

        self.btn_add.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)


class FeedbackMain(QWidget):
    def __init__(self):
        super().__init__()
        self.db = FeedbackManager()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Головний layout для цього екрану
        layout = QVBoxLayout(self)
        layout.setObjectName("layout")

        # Верхня панель (Заголовок і кнопка додавання)
        top_panel = QHBoxLayout()

        title = QLabel("Скарги - Пропозиції")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #fff;")

        self.btn_add = QPushButton("+ Новий запис")
        self.btn_add.setFixedWidth(200)
        self.btn_add.clicked.connect(self.open_add_feedback)

        top_panel.addWidget(title)
        top_panel.addStretch()  # Відштовхує кнопку вправо
        top_panel.addWidget(self.btn_add)

        # Таблиця
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Дата","Ім'я","Тип","Опис","Статус","Приорітет"])
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

    def load_data(self):
        """Очищає таблицю і заповнює її даними з бази"""
        self.table.setRowCount(0)  # Очищення старих рядків
        feedback = self.db.get_all_feedback()

        for row_idx, row_data in enumerate(feedback):
            self.table.insertRow(row_idx) # створення нового рядка
            id_feedback = row_data[0]
            date = row_data[1]

            # Колонка 0 додаєм туди дату замість індекса
            col_date = QTableWidgetItem(date)
            col_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Ховаємо id під датою
            col_date.setData(Qt.ItemDataRole.UserRole, id_feedback)
            self.table.setItem(row_idx, 0, col_date)

            mapping = [(1,2),(2,3),(3,4),(4,5),(5,7)]
            for ui_col, db_col in mapping:
                item_text = str(row_data[db_col]) if row_data[db_col] else ""
                cell_widget = QTableWidgetItem(item_text)
                cell_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, ui_col, cell_widget)

    def open_add_feedback(self):
        """зробити перевірки на введеня тексту"""
        dialog = AddFeedbackDialog(self)
        # данні з полів
        if dialog.exec() == QDialog.DialogCode.Accepted:
            t_type = dialog.option.currentText()
            author_name = dialog.author_name.text().strip() or "Анонім"
            t_priority = dialog.priority.currentText()
            text_feedback = dialog.text_feedback.toPlainText()

            if not text_feedback.strip(): # щоб не пропустити пробіл
                QMessageBox.warning(self,"Увага","Поле з причиною не може бути порожнім!")
                return

            # Запис в бд
            self.db.add_feedback(name_author=author_name, f_type=t_type, description=text_feedback, priority=t_priority)
            self.load_data()


    def show_context_menu(self):
        pass
