from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QLabel,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QTableWidgetItem, QLineEdit, QFileDialog
)

from PyQt6.QtCore import Qt,QUrl
from PyQt6.QtGui import QDoubleValidator, QPixmap, QDesktopServices
from src.UI.components.erm_table import ERMTable
import os  
import json




class TransactionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

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
        table_headers = ["Номер", "Дата", "Дія", "Категорія", "Сума"]
        self.table = ERMTable(columns=5, headers=table_headers)
        # Робимо так, щоб колонки автоматично розтягувалися на всю ширину
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addLayout(top_panel)
        layout.addWidget(self.table)


    def fill_table(self, transactions_data):
        """Приймає готовий список і просто малює його на екрані"""
        self.table.setRowCount(0)
        
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
        self.type_combo.addItems(["Витрати", "Дохід"])

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Наприклад: Продукти, Авто...")

        self.sum_input = QLineEdit()
        self.sum_input.setPlaceholderText("0.00")
        # Валідатор від 0.0 до 100000, максимум 2 знаки після коми
        validator = QDoubleValidator(0.0, 1000000.0, 2)
        # StandardNotation гарантує, що не буде експонеційного формату(типу 1е+06)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.sum_input.setValidator(validator)

        # Коментарій 
        self.comment = QTextEdit()
        self.comment.setPlaceholderText("Додатковий коментарій до транзакції (не обов'язково)")

        # Добавлення фактур 
        self.selected_file_path = [] # Тут будемо зберігати тимчасовий шлях
        layout_browse = QHBoxLayout()
        self.btn_browse = QPushButton("📎 Вибрати файли")
        self.lbl_file_name = QLabel("Файл не вибрано")
        self.lbl_file_name.setWordWrap(True)  # Додаємо перенесення тексту, якщо він довгий
        self.btn_browse.clicked.connect(self.select_file)


        #Кнопки
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти")
        self.btn_cancel = QPushButton("Скасувати")
        
        layout_browse.addWidget(self.btn_browse)
        layout_browse.addWidget(self.lbl_file_name)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addRow("Тип", self.type_combo)
        layout.addRow("Категорія", self.category_input)
        layout.addRow("Сума", self.sum_input)
        layout.addRow("Коментар", self.comment) 
        
        layout.addRow(layout_browse)  
        layout.addRow(btn_layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def select_file(self):
        """Відкриває вікно вибору файлів"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            # Повертає список шляхів (підчеркування в перемінй означає, що я знаю що повернеться другий аргумент але я його не буду використовувати, сміття)
            self,
            "Виберіть документи",
            "",
            "Документи та Зображення (*.pdf *.png *.jpg *.jpeg)"
        )
        # Перевірка на дублікати, попередження про те що додаємо 2 одинакових файли до транзакції
        if file_paths:
            for path in file_paths:
                if path in self.selected_file_path:
                    reply = QMessageBox.question(
                        self,
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    # Якщо користувач натиснув No просто пропускаємо файл і йдемо далі
                    if reply == QMessageBox.StandardButton.No:
                        continue
                self.selected_file_path.append(path)
        
        if self.selected_file_path:
            names = [f" {os.path.basename(p)}" for p in self.selected_file_path]
            self.lbl_file_name.setText("\n".join(names))

            

class EditTransactionDialog(QDialog):
    """Спливаюче вікно для редагування транзакції"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_files = []
        self.new_files_to_add = []
        self.setWindowTitle("Редагувати транзакцію")
        self.setFixedSize(850,400)

        layout = QFormLayout(self)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Витрати", "Дохід"])

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Наприклад: Продукти, Авто...")

        self.sum_input = QLineEdit()
        self.sum_input.setPlaceholderText("0.00")
        
        # Валідатор від 0.0 до 100000, максимум 2 знаки після коми
        validator = QDoubleValidator(0.0, 1000000.0, 2)
        
        # StandardNotation гарантує, що не буде експонеційного формату(типу 1е+06)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.sum_input.setValidator(validator)

        # Коментарій 
        self.comment = QTextEdit()
        self.comment.setPlaceholderText("Додатковий коментарій до транзакції (не обов'язково)")

        # Добавлення фактур 
        # Добавлення фактур 
        self.selected_file_path = None # Тут будемо зберігати тимчасовий шлях
        layout_browse = QHBoxLayout()
        self.btn_browse = QPushButton("📎 Вибрати файли")
        self.lbl_file_name = QLabel("Файли не вибрано")
        self.btn_browse.clicked.connect(self.select_file)

        #Кнопки
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти")
        self.btn_cancel = QPushButton("Скасувати")

        layout_browse.addWidget(self.btn_browse)
        layout_browse.addWidget(self.lbl_file_name)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addRow("Тип", self.type_combo)
        layout.addRow("Категорія", self.category_input)
        layout.addRow("Сума", self.sum_input)
        layout.addRow("Коментар", self.comment) 
        
        layout.addRow(layout_browse)  
        layout.addRow(btn_layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def fill_data(self, data):
        # Заповнює таблицю існуючими даними
        # data = (id, date, type, category, sum, comment, receipt_path)
        t_type = data[2]
        t_category = data[3]
        t_sum = data[4]
        t_comment = data[5]

        index = self.type_combo.findText(t_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)

        self.category_input.setText(str(t_category))
        self.sum_input.setText(str(t_sum))
        
        # Якщо коментар не None, вставляємо його
        if t_comment:
            self.comment.setText(str(t_comment))

        self.current_files = json.loads(data[6]) if data[6] else []
        self.refresh_file_list()

    def refresh_file_list(self):
        pass

    def select_file(self):
        """Відкриває вікно вибору файлу"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Виберіть документ",
            "",
            "Документи та Зображення (*.pdf *.png *.jpg *.jpeg)"
        )
        if file_path:
            self.selected_file_path = file_path
            # Показуємо користувачу тільки ім'я файлу, а не весь довгий шлях
            file_name = os.path.basename(file_path)
            self.lbl_file_name.setText(file_name)

class TransactionDetailsDialog(QDialog):
    """Модальне вікно для перегляду деталей транзакції (Тільки для читання)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Деталі транзакції")
        self.setFixedSize(400, 300) # Трохи збільшив вікно для нової кнопки

        # Змінна, де ми будемо зберігати шлях до файлу для цієї транзакції
        self.current_receipt_path = None 

        layout = QFormLayout(self)

        self.lbl_id = QLabel()
        self.lbl_date = QLabel()
        self.lbl_type = QLabel()
        self.lbl_category = QLabel()
        
        self.lbl_sum = QLabel()
        font = self.lbl_sum.font()
        font.setBold(True)
        self.lbl_sum.setFont(font)
        
        self.lbl_comment = QLabel()
        self.lbl_comment.setWordWrap(True)

        # --- Кнопка для відкриття фактури ---
        self.layout_path_file = QHBoxLayout()
        self.btn_open_receipt = QPushButton("📎 Відкрити фактуру")
        self.layout_path_file.addWidget(self.btn_open_receipt)
        # Підключаємо клік до методу відкриття файлу
        self.btn_open_receipt.clicked.connect(self.open_receipt_file) 

        layout.addRow("ID запису:", self.lbl_id)
        layout.addRow("Дата:", self.lbl_date)
        layout.addRow("Тип:", self.lbl_type)
        layout.addRow("Категорія:", self.lbl_category)
        layout.addRow("Сума:", self.lbl_sum)
        layout.addRow("Коментар:", self.lbl_comment)
        layout.addRow("Документ:", self.layout_path_file) # Додали в макет

        self.btn_close = QPushButton("Закрити")
        self.btn_close.clicked.connect(self.accept)
        layout.addRow("", self.btn_close)

    def fill_data(self, data):
        """Заповнює текстові мітки даними з бази"""
        # data = (id, date, type, category, sum, comment, receipt_path)
        self.lbl_id.setText(str(data[0]))
        self.lbl_date.setText(str(data[1]))
        self.lbl_type.setText(str(data[2]))
        self.lbl_category.setText(str(data[3]))
        self.lbl_sum.setText(f"{data[4]}")
        
        comment = data[5]
        self.lbl_comment.setText(str(comment) if comment else "—")

        # --- НОВЕ: Логіка для кнопки фактури ---
        receipt_paths = json.loads(data[6]) if data[6] else []
        
        if receipt_paths:
            for path in receipt_paths:
                if os.path.exists(path):
                    btn = QPushButton(f"📎 Відкрити: {os.path.basename(path)}")
                    btn.clicked.connect(lambda checked, p=path: self.open_file(p))
                    self.layout_path_file.addWidget(btn) # Додаємо в макет
                else:
                    self.layout_path_file.addWidget(QLabel(f"❌ Файл не знайдено: {os.path.basename(path)}"))
        else:
            self.layout_path_file.addWidget(QLabel("Немає прикріплених файлів"))

    def open_receipt_file(self):
        """Відкриває файл стандартною програмою ОС (наприклад, PDF-рідером)"""
        if self.current_receipt_path:
            # Перетворюємо звичайний шлях у формат URL, який розуміє QDesktopServices
            file_url = QUrl.fromLocalFile(os.path.abspath(self.current_receipt_path))
            QDesktopServices.openUrl(file_url)
    def open_file(self, path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(path)))