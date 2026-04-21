from src.DataBase.db_manager import BudgetsDB, CategoriesDB


class BudgetService:
    def __init__(self):
        self.db = BudgetsDB()
        self.cat_db = CategoriesDB()
        self.seed_initial_budget()  # Автоматично перевіряємо та заповнюємо при старті

    def get_budget_stats(self, year):
        """Звертається до бази і повертає статистику (Назва, План, Факт)"""
        return self.db.get_budget_stats(year)

    def seed_initial_budget(self):
        """Перевіряє, чи порожня база, і якщо так — заливає дані з кошторису"""
        # 1. Перевіряємо, чи є вже дані на 2026 рік
        existing_data = self.get_budget_stats(2026)
        if len(existing_data) > 0:
            return  # Якщо дані вже є, просто виходимо. База заповнена.

        print("Заповнюємо базу початковим бюджетом на 2026 рік...")

        # 2. Наш затверджений кошторис з PDF
        initial_data = {
            "Proveedores": 15000.00,
            "Ascensores": 3945.12,
            "Fumigación": 1200.00,
            "Mantenimiento puertas de garaje": 1338.24,
            "Mantenimiento extintores": 1196.00,
            "Mantenimiento y limpieza": 46149.72,
            "Entidad Urbanística de Conservación": 6533.44,
            "Reparaciones": 7000.00,
            "Administración": 8488.80,
            "Protección de datos": 45.00,
            "Otros profesionales": 100.00,
            "Seguro": 8500.00,
            "Comisiones bancarias": 500.00,
            "Correos": 100.00,
            "Electricidad": 22500.00,
            "Agua": 12000.00,
            "Basura y alcantarillado": 156.66,
            "Vado": 250.00,
            "Igic soportado": 8818.34,
            "Fondo de reserva 10%": 13600.00,
            "Internet porteros": 250.00,
            "Coordinación actividades empresariales": 130.00
        }

        # 3. Записуємо кожну категорію в базу
        for name, amount in initial_data.items():
            # Викликаємо метод запису (переконайся, що він є у твоєму BudgetsDB)
            self.db.set_budget(name, 2026, amount)

        print("База успішно заповнена!")

    def add_budget(self, name):
        pass