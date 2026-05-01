"""Логіка між базою даних і інтерфейсом"""

from src.DataBase.db_manager import BudgetsDB, CategoriesDB, TransactionManager
import os
import shutil
from datetime import datetime


class BudgetService:
    def __init__(self):
        self.db = BudgetsDB()
        self.cat_db = CategoriesDB()
        self.trans_db = TransactionManager()
        self.seed_initial_budget()

    def get_budget_stats(self, year):
        """Звертається до бази і повертає статистику (Назва, План, Факт)"""
        return self.db.get_budget_stats(year)
    def update_budget(self, category_name, year, new_amount):
        """Передає нову суму в базу даних"""
        self.db.update_budget_amount(category_name, year, new_amount)

    def seed_initial_budget(self):
        """Перевіряє, чи порожня база, і якщо так — заливає дані з кошторису"""
        # 1. Перевіряємо, чи є вже дані на 2026 рік
        existing_data = self.get_budget_stats(2026)
        if len(existing_data) > 0:
            return

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
            self.db.set_budget(name, 2026, amount)

        print("База успішно заповнена!")

    def add_payment(self, category_name, amount, date_str, receipt_path):
        """Зберігає платіж і копіює фактуру у внутрішню папку програми"""
        final_path = ""

        # Якщо шлях передали і такий файл дійсно існує на комп'ютері
        if receipt_path and os.path.exists(receipt_path):
            # Створюємо папку data/receipts, якщо її ще немає
            save_dir = "data/receipts"
            os.makedirs(save_dir, exist_ok=True)

            # Беремо оригінальну назву (напр. check.pdf)
            original_filename = os.path.basename(receipt_path)

            # Додаємо час до назви, щоб файли з однаковими іменами не перезаписали один одного
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{original_filename}"
            final_path = os.path.join(save_dir, safe_filename)

            # ФІЗИЧНО КОПІЮЄМО ФАЙЛ у нашу папку
            shutil.copy2(receipt_path, final_path)
            print(f"Фактуру збережено в: {final_path}")

        # Зберігаємо транзакцію в базу (передаємо новий, безпечний шлях)
        self.trans_db.add_transaction(
            trans_type="Витрата",
            category=category_name,
            amount=amount,
            status="Проведено",
            ai_details=None,
            receipt_path=final_path
        )

    def get_category_transactions(self, category_name, year):
        """Отримує всі витрати для вибраної категорії за вказаний рік"""
        with self.trans_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, date, sum, receipt_path 
                FROM transactions 
                WHERE category = ? AND type = 'Витрата' AND strftime('%Y', date) = ?
                ORDER BY date DESC
            """, (category_name, str(year)))
            return cursor.fetchall()

    def delete_transaction(self, t_id):
        """Видаляє транзакцію за її ID"""
        # Твій TransactionManager вже має цей метод
        self.trans_db.delete_transaction(t_id)