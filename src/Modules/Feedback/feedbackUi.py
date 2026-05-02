from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QTableWidgetItem, QLineEdit, QFileDialog
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

class EditFeedbackDialog(QDialog):
    def __init__(self, current_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редагування запису")
        self.setFixedSize(850, 650)

        # current_data - це рядок з БД: (id, date, name, type, description, status, resolution_note, priority, [file_path])
        form_layout = QFormLayout(self)

        self.option = QComboBox()
        self.option.addItems(["Скарга", "Пропозиція"])
        self.option.setCurrentText(current_data[3] if current_data[3] else "Скарга")

        self.author_name = QLineEdit()
        self.author_name.setText(current_data[2] if current_data[2] else "")

        self.priority = QComboBox()
        self.priority.addItems(["Високий", "Середній", "Низький"])
        self.priority.setCurrentText(current_data[7] if len(current_data) > 7 and current_data[7] else "Середній")

        self.status_cb = QComboBox()
        self.status_cb.addItems(["Нове", "В процесі", "Вирішено"])
        self.status_cb.setCurrentText(current_data[5] if len(current_data) > 5 and current_data[5] else "Нове")

        self.text_feedback = QTextEdit()
        self.text_feedback.setText(current_data[4] if len(current_data) > 4 and current_data[4] else "")

        # --- РОБОТА З ФАЙЛОМ ---
        self.file_path_input = QLineEdit()
        # Безпечно беремо файл, якщо колонка вже існувала
        current_file = current_data[8] if len(current_data) > 8 and current_data[8] else ""
        self.file_path_input.setText(current_file)

        self.btn_browse = QPushButton("📁 Вибрати файл")
        self.btn_browse.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.btn_browse)

        # --- КНОПКИ ---
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти зміни")
        self.btn_cancel = QPushButton("Скасувати")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        form_layout.addRow("Тип:", self.option)
        form_layout.addRow("Ім'я автора:", self.author_name)
        form_layout.addRow("Важливість:", self.priority)
        form_layout.addRow("Статус:", self.status_cb)
        form_layout.addRow("Опис:", self.text_feedback)
        form_layout.addRow("Прикріплений файл:", file_layout)
        form_layout.addRow(btn_layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Вибрати файл", "", "All Files (*);;PDF (*.pdf);;Images (*.png *.jpg)")
        if file_name:
            self.file_path_input.setText(file_name)