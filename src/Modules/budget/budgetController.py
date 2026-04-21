from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.Modules.budget.budgetUi import BudgetWindow
from src.Modules.budget.budgetService import BudgetService


class BudgetController(QWidget):
    def __init__(self):
        super().__init__()
        print("1. BudgetController успішно створено!")

        # 1. Створюємо інтерфейс та сервіс даних
        self.ui = BudgetWindow()
        self.service = BudgetService()

        # 2. Розміщуємо інтерфейс на екрані контролера
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Прибираємо зайві відступи
        layout.addWidget(self.ui)

        # 3. Даємо команду завантажити дані
        self.load_data()

    def load_data(self):
        print("2. Контролер просить дані у сервісу...")

        # Звертаємося до сервісу (він дістає дані з бази)
        data = self.service.get_budget_stats(2026)

        print(f"3. Отримано записів з БД: {len(data)}")

        # Передаємо дані в UI для малювання таблиці
        if data:
            self.ui.fill_table(data)
            print("4. Таблиця успішно заповнена!")
        else:
            print("Увага: База даних порожня!")