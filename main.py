import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QTableWidget, QHeaderView, QStackedWidget)
from PyQt6.QtCore import Qt

from ui.FeedbackMain import FeedbackDiaolog
from ui.Sidebar import Sidebar
from ui.Dashboard import Dashboard
from ui.Transactions import Transactions




class ERMMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ERM")
        self.resize(1750, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.setObjectName("main_layout")
        central_widget.setLayout(main_layout)

        #left side
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        #Ініціалізація всіх сторінок
        self.dashboard = Dashboard()
        self.transaction_view = Transactions()
        # self.feedback = FeedbackDiaolog()
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.transaction_view)
        # self.content_stack.addWidget(self.feedback)


        # Підключення сигналу від sidebar
        self.setup_connections()

    def setup_connections(self):
        """Тут ми пов'язуємо кнопки сайдбару з перемиканням екранів"""
        # Приклад: якщо в Sidebar є кастомний сигнал або відкритий доступ до кнопок
        # Lambda - для того щоб переключати екран тільки тоді коли натискається кнопка а не відразу після запуску програми
        self.sidebar.btn_dashboard.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.sidebar.btn_transactions.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.sidebar.btn_feedback.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))

def load_styles(style):
    """
        Download styles
        :param style:
        :return:
    """
    try:
        with open("ui/style/style.qss", "r", encoding="utf-8") as style_file:
            style_content = style_file.read()
            style.setStyleSheet(style_content)
    except FileNotFoundError:
        print("⚠️ Файл стилів style.qss не знайдено! Використовується стандартна тема.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_styles(app)

    window = ERMMainWindow()
    window.show()
    sys.exit(app.exec())