import sqlite3
import os
import sys
import json
from datetime import datetime

# --- ШЛЯХ ДО БАЗИ ДАНИХ ---
if getattr(sys, 'frozen', False):
    # Якщо програма запущена як зібраний .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Якщо запущена через код (PyCharm/VS Code)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Створюємо папку data поруч із програмою, якщо її немає
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Точний абсолютний шлях до файлу БД
DB_PATH = os.path.join(DATA_DIR, "database.db")

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH

    def get_connection(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)


class RegularPaymentsDB(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS regular_payments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                day_of_month INTEGER NOT NULL
               )  
            """)
            conn.commit()

    def add_regula_payment(self, name, amount, category, day):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO regular_payments(name, amount, category, day_of_month) VALUES(?,?,?,?)
            """, (name, amount, category, day))
            conn.commit()

    def get_all_regular_payments(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT name,amount,category,day_of_month FROM regular_payments""")
            return cursor.fetchall()

class UsersDB(DatabaseManager):
    def __init__(self,db_path=None):
        super().__init__(db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email,
                    password
                    )
                """)
            conn.commit()

class CategoriesDB(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE)
            """)
            conn.commit()

            default_categories = [
                "Proveedores",
                "Ascensores",
                "Fumigación",
                "Mantenimiento puertas de garaje",
                "Mantenimiento extintores",
                "Mantenimiento y limpieza",
                "Entidad Urbanística de Conservación",
                "Reparaciones",
                "Administración",
                "Protección de datos",
                "Otros profesionales",
                "Seguro",
                "Comisiones bancarias",
                "Correos",
                "Electricidad",
                "Agua",
                "Basura y alcantarillado",
                "Vado",
                "Igic soportado",
                "Fondo de reserva 10%",
                "Sanciones tributarias",
                "Internet porteros",
                "Coordinación actividades empresariales"
            ]

            for cat_name in default_categories:
                cursor.execute("""
                    INSERT OR IGNORE INTO categories(name) VALUES(?)
                """, (cat_name,))
                conn.commit()

class BudgetsDB(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    allocated_amount INTEGER NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
                    UNIQUE (category_id, year))
            """)

            conn.commit()

    def set_budgets(self,category_id,year,amount):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id FROM budget WHERE name = ?""", (category_id,))
            res = cursor.fetchone()
            if res:
                cat_id = res[0]
                cursor.execute("""
                INSERT OR REPLACE INTO budgets(category_id, year, allocated_amount) 
                VALUES(?,?,?)""", (cat_id,year, abs(amount)))
                conn.commit()

    def set_budget(self, category_name, year, amount):
        """Встановлює суму бюджету для категорії за назвою"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Шукаємо ID категорії
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            res = cursor.fetchone()
            if res:
                cat_id = res[0]
                # Записуємо бюджет
                cursor.execute("""
                    INSERT OR IGNORE INTO budgets (category_id, year, allocated_amount)
                    VALUES (?, ?, ?)
                """, (cat_id, year, amount))
            conn.commit()

    def get_budget_stats(self, year):
        """Об'єднує категорії, бюджети та реальні транзакції в один список для UI"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Беремо план з budgets, а витрати сумуємо з transactions
            cursor.execute("""
                SELECT 
                    c.name, 
                    b.allocated_amount, 
                    COALESCE(SUM(t.sum), 0) as spent
                FROM budgets b
                JOIN categories c ON b.category_id = c.id
                LEFT JOIN transactions t ON c.name = t.category 
                    AND strftime('%Y', t.date) = CAST(b.year AS TEXT)
                WHERE b.year = ?
                GROUP BY c.id
            """, (year,))
            return cursor.fetchall()

    def update_budget_amount(self, category_name, year, new_amount):
        """Оновлення бюджету вибраної категорії"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Знаходимо id категорії
            cursor.execute("""SELECT id FROM categories WHERE name = ?""", (category_name,))
            res = cursor.fetchone()
            if res:
                # якщо res найдено тоді cat_id буде дорівнювати 1 елементу тобто id res[0]
                cat_id = res[0]
                # 2.Оновлюємо суму
                cursor.execute("""
                    UPDATE budgets SET allocated_amount = ?
                    WHERE category_id = ? AND year = ?
                """,(new_amount,cat_id,year))
            conn.commit()

class DashboardManager(DatabaseManager):
    def __init__(self, db_path=None):
        super().__init__(db_path)
        self.init_db()




