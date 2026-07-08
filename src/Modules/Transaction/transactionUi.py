from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QTableWidgetItem, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt

class TransactionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Виклик побудови інтерфейсу

    def setup_ui(self):
        print("Ok")
        # Головний layout для цього екрану
        layout = QVBoxLayout(self)
        layout.setObjectName("layout")

        # Верхня панель (Заголовок і кнопка додавання)
        top_panel = QHBoxLayout()
        title= QLabel("Транзакції")
        
        # Кнопки(верхній сайдбар)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Пошук...")
        self.search_input.setClearButtonEnabled(True)
        # Функція автоматичного пошуку при заповнені
        #self.search_input.textChanged.connect()


        self.btn_add = QPushButton("+ Додати транзакцію")
        self.btn_add.setFixedWidth(200)


        top_panel.addWidget(title) 
        top_panel.addWidget(self.search_input)
        top_panel.addStretch()  # Відштовхує кнопку вправо
        top_panel.addWidget(self.btn_add)
        # -----------------------------------------------------------
        
        # # Таблиця
        # self.table = QTableWidget(0, 6)
        # self.table.setHorizontalHeaderLabels(["Номер", "Дата", "Тип", "Категорія", "Сума", "Статус"])
        # # self.table.setColumnWidth(6,160)

        # # Робимо так, щоб колонки автоматично розтягувалися на всю ширину
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # # Дозвіл на кастомне контекстн меню
        # self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # # Підключення сигнала правого натискання мишки
        # self.table.customContextMenuRequested.connect(self.show_context_menu)
        # self.table.verticalHeader().setVisible(False)

        layout.addLayout(top_panel)
        # layout.addWidget(self.table)
        


