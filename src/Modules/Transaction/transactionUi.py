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
        self.setup_ui()

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
        # self.search_input.textChanged.connect()

    
        self.export_button = QPushButton("Експорт в PDF/CSV")
        self.export_button.setFixedWidth(200)

        self.import_button = QPushButton("Імпорт з PDF/CSV")
        self.import_button.setFixedWidth(200)

        self.btn_add = QPushButton("+ Додати транзакцію")
        self.btn_add.setFixedWidth(200)


        top_panel.addWidget(title) 
        top_panel.addStretch()
        top_panel.addWidget(self.search_input)
        top_panel.addWidget(self.import_button)
        top_panel.addWidget(self.export_button)
        top_panel.addWidget(self.btn_add)
        # -----------------------------------------------------------
        
        # Таблиця
        table_headers = ["Дата","Тип","Категорія","Сума","Статус"]
        self.table = ERMTable(columns=5, headers=table_headers)
        
        layout.addLayout(top_panel)
        layout.addWidget(self.table)


    def fill_table(self, transactions_data):
        """Приймає готовий список і просто малює його на екрані"""
        self.table.setRowCount(0)
        
        # Твій оригінальний цикл переїжджає сюди, але працює з переданим списком
        for row_idx, row_data in enumerate(transactions_data):
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
        


