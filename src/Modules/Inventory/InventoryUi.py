from PyQt6.QtWidgets import QFrame, QVBoxLayout


class InventoryWindow(QFrame):
    def __init__(self):
        super().__init__()


        self.setObjectName("content_area")

        #Main window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(main_layout)