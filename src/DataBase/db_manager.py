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

    # def get_budget_by_year(self,year):
    #     with self.get_connection() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("""
    #             SELECT c.name, b.allocated_amount
    #             FROM budgets b
    #             JOIN categories c ON c.category_id = b.id
    #             WHERE b.year = ?
    #             ORDER BY b.allocated_amount DESC
    #         """,(year,))
    #         conn

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
        """Об'єднує категорії та бюджети в один список для UI"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.name, b.allocated_amount, 0 -- 0 це заглушка для фактичних витрат
                FROM budgets b
                JOIN categories c ON b.category_id = c.id
                WHERE b.year = ?
            """, (year,))
            return cursor.fetchall()




