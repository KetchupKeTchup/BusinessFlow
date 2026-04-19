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

# В розробці
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
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
            """)
            conn.commit()

class BudgetsDB(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    FOREIGN KEY (category) REFERENCES categories(category_id) ON DELETE CASCADE,
                    year INTEGER NOT NULL,
                    allocated_amount INTEGER NOT NULL
            """)
            conn.commit()