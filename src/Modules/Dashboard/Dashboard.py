from PyQt6.QtWidgets import QFrame, QVBoxLayout


class Dashboard(QFrame):
    def __init__(self):
        super().__init__()

        #Main window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(main_layout)
