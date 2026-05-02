
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTableWidgetItem,
    QDialog, QDoubleSpinBox, QComboBox, QDateEdit, QLineEdit, QFileDialog,QButtonGroup,QRadioButton,QHeaderView,QTableWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import  QPainter
from PyQt6.QtCharts import QChart, QChartView
from src.UI.components.erm_table import ERMTable


class BudgetWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # --- 1. ХЕДЕР (Верхня панель) ---
        header = QHBoxLayout()
        title = QLabel("$ Планування бюджету")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color:#fff")

        self.year_selector = QComboBox()
        self.year_selector.addItems(["2026", "2027", "2028", "2029", "2030"])
        self.year_selector.setCurrentText("2026")  # За замовчуванням

        self.btn_add_payment = QPushButton("+ Додати")
        self.btn_add_payment.setFixedWidth(200)

        header.addWidget(title)
        header.addWidget(self.year_selector)
        header.addStretch()
        header.addWidget(self.btn_add_payment)

        # --- 2. ТАБЛИЦЯ ---
        headers = ["Categoría", "Previsto (2026)", "Gastado", "Resto"]
        self.table = ERMTable(columns=4, headers=headers)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # --- 3. ГРАФІК ТА КНОПКИ ---
        self.chart = QChart()
        self.chart.setTitle("Розподіл бюджету")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundVisible(False)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        from PyQt6.QtWidgets import QRadioButton, QButtonGroup
        self.radio_plan = QRadioButton("План")
        self.radio_fact = QRadioButton("Витрати")
        self.radio_plan.setChecked(True)
        self.radio_plan.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.radio_fact.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")

        self.chart_type_group = QButtonGroup()
        self.chart_type_group.addButton(self.radio_plan)
        self.chart_type_group.addButton(self.radio_fact)

        radio_layout = QHBoxLayout()
        radio_layout.addStretch()
        radio_layout.addWidget(self.radio_plan)
        radio_layout.addSpacing(20)  # Відступ між кнопками
        radio_layout.addWidget(self.radio_fact)
        radio_layout.addStretch()

        chart_container = QVBoxLayout()
        chart_container.addLayout(radio_layout)
        chart_container.addWidget(self.chart_view)

        # --- 4. ЗБИРАЄМО ТІЛО (Таблиця + Графік) ---
        body_layout = QHBoxLayout()
        body_layout.addWidget(self.table, stretch=6)  # Таблиця займає 60%
        body_layout.addLayout(chart_container, stretch=4)  # Графік з кнопками - 40%

        # --- 5. ПІДВАЛ (Загальна сума) ---
        self.lbl_total = QLabel("Cantidad total: 0.00 €")
        self.lbl_total.setStyleSheet("font-size: 20px; font-weight: bold; color:#fff; margin-top: 10px;")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --- 6. ФІНАЛЬНА ЗБІРКА ВІКНА ---
        main_layout.addLayout(header)
        main_layout.addLayout(body_layout)
        main_layout.addWidget(self.lbl_total)
        self.setLayout(main_layout)


    def fill_table(self, data_list):
        """Цей метод просто бере список і заповнює таблицю"""
        self.table.setRowCount(0)
        if not data_list:
            return

        # self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data_list):
            self.table.insertRow(row_idx)

            # Очікуємо 3 параметри: назва, план, факт
            name, planned, spent = row_data
            remaining = planned - spent

            name_item = QTableWidgetItem(str(name))
            plan_item = QTableWidgetItem(f"{planned:,.2f} €")
            spent_item = QTableWidgetItem(f"{spent:,.2f} €")
            rem_item = QTableWidgetItem(f"{remaining:,.2f} €")

            for item in [plan_item, spent_item, rem_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            if remaining < 0:
                rem_item.setForeground(Qt.GlobalColor.red)

            self.table.setItem(row_idx, 0, name_item)
            self.table.setItem(row_idx, 1, plan_item)
            self.table.setItem(row_idx, 2, spent_item)
            self.table.setItem(row_idx, 3, rem_item)

class EditBudgetDialog(QDialog):
    # щас init приймає параметри
    def __init__(self, category_name, current_amount_str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edición{category_name}")
        self.setFixedSize(850,400)

        layout = QVBoxLayout(self)

        # Поле введення суми
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(9999999.00)
        # Очищаємо рядок "15,000.00$" ід ком і валюти
        clean_amount = current_amount_str.replace(' €', '').replace(',', '')
        self.amount_input.setValue(float(clean_amount))

        # buttons
        btn_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Ahorrar") # Зберегити
        self.btn_cancel = QPushButton("Cancelar") # Скасувати
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        # Збираємо все докупи
        layout.addWidget(QLabel("Введіть новий план на рік:"))
        layout.addWidget(self.amount_input)
        layout.addLayout(btn_layout)

        # Підключаємо дії (вбудовані методи QDialog)
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

class AddTransactionDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo pago (Новий платіж)")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        self.category_cb = QComboBox()
        self.category_cb.addItems(categories)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(9999999.00)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Файл не вибрано...")
        self.btn_browse = QPushButton("📁")
        self.btn_browse.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.btn_browse)

        self.btn_save = QPushButton("Guardar (Зберегти)")
        self.btn_save.clicked.connect(self.accept)

        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.category_cb)
        layout.addWidget(QLabel("Cantidad (€):"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Factura (PDF/Imagen):"))
        layout.addLayout(file_layout)
        layout.addSpacing(15)
        layout.addWidget(self.btn_save)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Вибрати фактуру", "", "All Files (*);;PDF (*.pdf);;Images (*.png *.jpg)")
        if file_name:
            self.file_path_input.setText(file_name)

class TransactionHistoryDialog(QDialog):
    def __init__(self, category_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Історія витрат: {category_name}")
        self.setFixedSize(500, 300)
        self.layout = QVBoxLayout(self)

        # Створюємо таблицю
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "Сума (€)","Фактура", "Дія"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)  # Ховаємо технічний ID бази даних

        self.layout.addWidget(self.table)

        # Кнопка закриття
        self.btn_close = QPushButton("Закрити")
        self.btn_close.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_close)


