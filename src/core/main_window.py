
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget)
from src.Modules.Sidebar.Sidebar import Sidebar
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

    def add_page(self, widget):
        self.content_stack.addWidget(widget)

    def set_page(self, widget):
        self.content_stack.setCurrentWidget(widget)

