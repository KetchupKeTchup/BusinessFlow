from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QTableWidgetItem, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt

class TransactionWindow(QWidget):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
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

        


