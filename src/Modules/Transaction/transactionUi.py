from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QTableWidgetItem, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from src.UI.components.erm_table import ERMTable

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
        top_panel.addStretch()
        top_panel.addWidget(self.search_input)
        top_panel.addWidget(self.btn_add)
        # -----------------------------------------------------------
        
        # Таблиця
        table_headers = ["Дата","Тип","Категорія","Сума","Статус"]
        self.table = ERMTable(columns=5, headers=table_headers)
        
        layout.addLayout(top_panel)
        layout.addWidget(self.table)

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
        


