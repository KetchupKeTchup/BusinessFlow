from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class Sidebar(QFrame):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(300)
        self.setObjectName("Sidebar")

        layout = QVBoxLayout()
        layout.setContentsMargins(25,15,10,25)
        layout.setSpacing(10)
        self.setLayout(layout)


        # Buttons
        self.btn_dashboard = QPushButton("Menu")
        self.btn_transactions = QPushButton("💸 Транзакції")
        self.btn_documents = QPushButton("📁 Документи")
        self.btn_feedback = QPushButton("💬 Пропозиції/Скарги")
        self.btn_inventory = QPushButton("📦 Склад")
        self.btn_work_planning = QPushButton("🗓️ ️Планування робіт")

        buttons = [self.btn_dashboard,self.btn_transactions,self.btn_feedback,self.btn_inventory,self.btn_work_planning]

        for btn in buttons:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
        layout.addStretch()