from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit,
    QMessageBox, QTableWidgetItem, QLineEdit
)
from PyQt6.QtCore import Qt

# Змінили назву на FeedbackWindow, щоб збігалося з Контролером
class FeedbackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui() # Повернули виклик побудови інтерфейсу

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
        # Підключення кліку прибрали звідси (це робить Контролер)

        top_panel.addWidget(title)
        top_panel.addStretch()  # Відштовхує кнопку вправо
        top_panel.addWidget(self.btn_add)

        # Таблиця
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Дата","Ім'я","Тип","Опис","Статус","Приорітет"])

        # Робимо так, щоб колонки автоматично розтягувалися на всю ширину
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Дозвіл на кастомне контекстне меню (саме підключення меню робить Контролер)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.verticalHeader().setVisible(False)

        # Додаємо все на головний екран модуля
        layout.addLayout(top_panel)
        layout.addWidget(self.table)


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