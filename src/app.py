from src.core.main_window import ERMMainWindow
# Modules
from src.Modules.Feedback.FeedbackMain import FeedbackMain
from src.Modules.Dashboard.Dashboard import Dashboard
from src.Modules.Transaction.Transactions import Transactions
from src.Modules.RegularPayments.RegularPaymentsUi import RecurringPaymentWindow
from src.Modules.Inventory.InventoryUi import InventoryWindow


class App:
    def __init__(self):
        self.main_window = ERMMainWindow()
        # Створення модулів
        self._init_modules()
        # Реєстрація сторінок
        self._register_pages()
        # Налаштування навігації
        self._setup_navigation()

    def _init_modules(self):
        self.dashboard = Dashboard()
        self.transaction_view = Transactions()
        self.feedback = FeedbackMain()
        self.inventory = InventoryWindow()
        self.payments = RecurringPaymentWindow()

    def _register_pages(self):
        self.pages = {
            "dashboard": self.dashboard,
            "transactions": self.transaction_view,
            "feedback": self.feedback,
            "inventory": self.inventory,
            "payments": self.payments,
        }
        for page in self.pages.values():
            self.main_window.add_page(page)

    def _setup_navigation(self):
        sidebar = self.main_window.sidebar
        sidebar.btn_dashboard.clicked.connect(lambda: self.navigate("dashboard"))
        sidebar.btn_transactions.clicked.connect(lambda: self.navigate("transactions"))
        sidebar.btn_feedback.clicked.connect(lambda: self.navigate("feedback"))
        sidebar.btn_inventory.clicked.connect(lambda: self.navigate("inventory"))
        sidebar.btn_payment.clicked.connect(lambda: self.navigate("payments"))

    def navigate(self, page_name: str):
        """Перемикання сторінок по імені"""
        page = self.pages.get(page_name)
        if page:
            self.main_window.set_page(page)

    def run(self):
        self.main_window.show()