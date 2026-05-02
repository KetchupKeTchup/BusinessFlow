from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QChart, QChartView
from PyQt6.QtGui import QPainter


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Привітання
        title = QLabel("👋 Вітаємо у BusinessFlow Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white; margin-bottom: 20px;")
        self.layout.addWidget(title)

        # Контейнер для карток
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # --- КАРТКА 1: БЮДЖЕТ ---
        self.card_budget = QFrame()
        self.card_budget.setStyleSheet("background-color: #2c3e50; border-radius: 15px; padding: 20px;")
        budget_layout = QVBoxLayout(self.card_budget)
        budget_title = QLabel("💰 Бюджет 2026")
        budget_title.setStyleSheet("font-size: 18px; color: #bdc3c7;")
        self.lbl_budget_val = QLabel("Завантаження...")
        self.lbl_budget_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #2ecc71;")
        budget_layout.addWidget(budget_title)
        budget_layout.addWidget(self.lbl_budget_val)
        budget_layout.addStretch()

        # --- КАРТКА 2: ЗАВДАННЯ ---
        self.card_tasks = QFrame()
        self.card_tasks.setStyleSheet("background-color: #2c3e50; border-radius: 15px; padding: 20px;")
        tasks_layout = QVBoxLayout(self.card_tasks)
        tasks_title = QLabel("📋 Відкриті завдання")
        tasks_title.setStyleSheet("font-size: 18px; color: #bdc3c7;")
        self.lbl_tasks_val = QLabel("Завантаження...")
        self.lbl_tasks_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #e74c3c;")
        tasks_layout.addWidget(tasks_title)
        tasks_layout.addWidget(self.lbl_tasks_val)
        tasks_layout.addStretch()

        cards_layout.addWidget(self.card_budget)
        cards_layout.addWidget(self.card_tasks)

        self.layout.addLayout(cards_layout)

        # --- ГРАФІК СТАТУСІВ ---
        self.chart = QChart()
        self.chart.setTitle("📊 Статистика завдань")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundVisible(False)
        self.chart.setTitleBrush(Qt.GlobalColor.white)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;")

        # ОСЬ МАГІЧНИЙ РЯДОК, ЯКИЙ НЕ ДАСТЬ ГРАФІКУ ЗНИКНУТИ
        self.chart_view.setMinimumHeight(350)

        self.layout.addWidget(self.chart_view)

        # Stretch має бути в самому кінці, щоб штовхати все наверх!
        self.layout.addStretch()