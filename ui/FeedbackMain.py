from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit,
    QMessageBox, QMenu, QTableWidgetItem, QLineEdit
)
from PyQt6.QtCore import Qt
from src.db_manager import DatabaseManager

class AddFeedbackDiaolog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Додати нову Скаргу або Пропозицію")
        self.setFixedSize(850,600)

        layout = QVBoxLayout(self)

        self.option = QComboBox()
        self.option.addItems(["Скарга", "Пропозиція"])

        self.author_name = QLineEdit()
        self.author_name.setPlaceholderText("Вкажіть ім'я.")

        self.priority = QComboBox()
        self.priority.addItems(["Важливо", "Не терміново"])

        self.text_feedback = QTextEdit()

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Додати")

        layout.addRow("Вибір",self.option)
        layout.addRow("Ім'я хто запропонував", self.author_name)
        layout.addRow("Важливість", self.priority)
        layout.addRow("Опис", self.text_feedback)
        self.btn_add.clicked.connect(self.accept)



class FeedbackDiaolog(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.load_data()
        self.setup_ui()

    def setup_ui(self):
        # Головний layout для цього екрану
        layout = QVBoxLayout(self)
        layout.setObjectName("layout")

        # Верхня панель (Заголовок і кнопка додавання)
        top_panel = QHBoxLayout()

        title = QLabel("Скарги - Пропозиції")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #000; color:#fff")

        self.btn_add = QPushButton("+ Новий запис")
        self.btn_add.setFixedWidth(200)
        self.btn_add.clicked.connect(self.open_add_feedback)

        top_panel.addWidget(title)
        top_panel.addStretch()  # Відштовхує кнопку вправо
        top_panel.addWidget(self.btn_add)

        # Таблиця
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Номер","Дата","Ім'я", "Тип", "Опис", "Статус"])
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
        transactions = self.db.get_all_feedback() # отримання всіх даних

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

    def open_add_feedback(self):
        """зробити перевірки на введеня тексту"""
        dialog = AddFeedbackDiaolog(self)
        # данні з полів
        if dialog.exec() == QDialog.DialogCode.Accepted:
            t_type = dialog.option.currentText()
            author_name = dialog.author_name.text()
            priority = dialog.priority.currentText()
            text_feedback = dialog.text_feedback.toPlainText()

            # Запис в бд
            self.db.add_feedback(name_author=author_name,f_type=t_type,description=text_feedback, priority=priority)
            self.load_data()
