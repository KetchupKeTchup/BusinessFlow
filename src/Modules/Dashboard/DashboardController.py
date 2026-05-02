from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.Modules.Dashboard.DashboardUi import DashboardWindow
from src.Modules.Dashboard.DashboardServise import DashboardServise
from PyQt6.QtCharts import QPieSeries


class DashboardController(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = DashboardWindow()
        self.service = DashboardServise()

        # Розміщуємо інтерфейс
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        # Завантажуємо дані при старті
        self.load_statistics()

    def load_statistics(self):
        """Отримує дані з сервісу і вставляє в UI (картки та графік)"""
        # --- 1. ОНОВЛЕННЯ КАРТКИ ЗАВДАНЬ ---
        tasks_count = self.service.get_pending_tasks_count()
        self.ui.lbl_tasks_val.setText(f"{tasks_count} шт.")

        # --- 2. ОНОВЛЕННЯ КАРТКИ БЮДЖЕТУ ---
        budget_remaining = self.service.get_budget_summary(2026)
        self.ui.lbl_budget_val.setText(f"{budget_remaining:,.2f} €")

        # Якщо бюджет в мінусі - робимо колір червоним, якщо в плюсі - зеленим
        if budget_remaining < 0:
            self.ui.lbl_budget_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #e74c3c;")
        else:
            self.ui.lbl_budget_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #2ecc71;")

        # --- 3. ОНОВЛЕННЯ ГРАФІКА СТАТУСІВ ---
        from PyQt6.QtCharts import QPieSeries  # Імпортуємо тут, щоб точно не загубилося
        from PyQt6.QtCore import Qt

        status_counts = self.service.get_feedback_status_counts()
        print("Дані для графіка:", status_counts)  # Виводимо в термінал, щоб перевірити, чи є дані

        # Очищаємо старий графік перед нанесенням нових даних
        self.ui.chart.removeAllSeries()

        # Якщо база повернула хоч якісь дані — будуємо пиріг
        if status_counts:
            series = QPieSeries()
            for status, count in status_counts:
                # Захист від порожніх значень
                safe_status = status if status else "Невідомо"

                # Додаємо шматочок (Назва + Кількість)
                slice_obj = series.append(f"{safe_status} ({count})", count)

                # Налаштовуємо зовнішній вигляд підписів
                slice_obj.setLabelVisible(True)
                slice_obj.setLabelColor(Qt.GlobalColor.white)

            # Додаємо готову серію шматочків у сам графік
            self.ui.chart.addSeries(series)

    def showEvent(self, event):
        """
        Магія PyQt: Цей метод спрацьовує АВТОМАТИЧНО кожного разу,
        коли користувач перемикається на цю вкладку в боковому меню.
        """
        super().showEvent(event)  # Дозволяємо системі показати вікно
        self.load_statistics()  # Одразу тягнемо свіжі цифри з бази даних!