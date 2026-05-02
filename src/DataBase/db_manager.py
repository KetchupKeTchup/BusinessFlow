import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or "data/erm_database.db"

    def get_connection(self):
        return sqlite3.connect(self.db_path)

class TransactionManager(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        """Create the databese if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                sum REAL NOT NULL,
                status TEXT DEFAULT 'Заплановано',
                json_datails TEXT,
                receipt_path TEXT
            )
            """)
            conn.commit()
            print("Database created successfully")

    def add_transaction(self, trans_type, category, amount, status="Проведено", ai_details = None, receipt_path= None):
        """Add a transaction to the database"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_str = json.dumps(ai_details) if ai_details else None

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions(date, type, category, sum, status, json_datails, receipt_path)
                VALUES(?,?,?,?,?,?,?)
            """, (current_date, trans_type, category, amount, status, json_str, receipt_path))
            conn.commit()
            print(f"Transaction {amount} added successfully")

    def delete_transaction(self, t_id):
        """Delete a transaction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM transactions WHERE id = ?""",(t_id,))
            conn.commit()
            print(f"Transaction {t_id} deleted successfully")

    def get_all_transactions(self):
        """Get all transactions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id,date,type, category, sum, status FROM transactions ORDER BY date DESC
                """)
            return cursor.fetchall()

class FeedbackManager(DatabaseManager):
    def __init__(self,db_path=None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        """Create the databese for feedback if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT DEFAULT 'Нове',
                    resolution_note TEXT,
                    priority TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_feedback(self, name_author, f_type, description,priority):
        """Adds a new feedback"""
        curren_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback(date, name, type, description, status, resolution_note, priority) VALUES (?, ?, ?, ?, ?, ?, ?)""", (curren_data, name_author, f_type, description, "New", "", priority))
            conn.commit()

    def get_all_feedback(self):
        """Gets all feedback"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id, date, name, type, description, status, resolution_note, priority FROM feedback""")
            return cursor.fetchall()

    def update_status(self, feedback_id, new_status):
        """Оновлює статус звернення (скарги/пропозиції) за його ID"""
        # Використовуємо підключення до БД (переконайся, що get_connection() написано так, як в інших твоїх методах)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE feedback 
                SET status = ? 
                WHERE id = ?
            """, (new_status, feedback_id))
            conn.commit()
            print(f"Статус запису з ID {feedback_id} успішно змінено на '{new_status}'")

    def get_feedback_by_id(self, f_id):
        """Отримує всі дані одного запису для заповнення вікна редагування"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (f_id,))
            return cursor.fetchone()

    def update_feedback_full(self, f_id, name, f_type, desc, priority, status, file_path):
        """Оновлює абсолютно всі поля, включно з файлом. Якщо колонки файлу немає - створює її."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Спроба оновити всі поля
                cursor.execute("""
                    UPDATE feedback 
                    SET name = ?, type = ?, description = ?, priority = ?, status = ?, file_path = ?
                    WHERE id = ?
                """, (name, f_type, desc, priority, status, file_path, f_id))
            except Exception as e:
                # Якщо таблиця стара і в ній ще немає колонки file_path
                if "no such column: file_path" in str(e).lower():
                    cursor.execute("ALTER TABLE feedback ADD COLUMN file_path TEXT")
                    # Повторюємо запит після створення колонки
                    cursor.execute("""
                        UPDATE feedback 
                        SET name = ?, type = ?, description = ?, priority = ?, status = ?, file_path = ?
                        WHERE id = ?
                    """, (name, f_type, desc, priority, status, file_path, f_id))
                else:
                    raise e
            conn.commit()

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




