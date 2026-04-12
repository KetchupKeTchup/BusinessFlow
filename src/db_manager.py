import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self,db_transaction="data/db_transaction.db",db_feedback="data/db_feedback.db"):
        self.db_transaction = db_transaction
        self.db_feedback = db_feedback
        self.init_db_transaction()
        self.init_db_feedback()

    def get_connection_transaction(self):
        return sqlite3.connect(self.db_transaction)
    def get_connection_feedback(self):
        return sqlite3.connect(self.db_feedback)

    def init_db_transaction(self):
        """Create the databese if it doesn't exist"""
        with self.get_connection_transaction() as conn:
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

    def init_db_feedback(self):
        """Create the databese for feedback if it doesn't exist"""
        with self.get_connection_feedback() as conn:
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

    def add_transaction(self, trans_type, category, amount, status="Проведено", ai_details = None, receipt_path= None):
        """Add a transaction to the database"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_str = json.dumps(ai_details) if ai_details else None

        with self.get_connection_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions(date, type, category, sum, status, json_datails, receipt_path)
                VALUES(?,?,?,?,?,?,?)
            """, (current_date, trans_type, category, amount, status, json_str, receipt_path))
            conn.commit()
            print(f"Transaction {amount} added successfully")

    def delete_transaction(self, t_id):
        """Delete a transaction"""
        with self.get_connection_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM transactions WHERE id = ?""",(t_id,))
            conn.commit()
            print(f"Transaction {t_id} deleted successfully")

    def get_all_transactions(self):
        """Get all transactions"""
        with self.get_connection_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id,date,type, category, sum, status FROM transactions ORDER BY date DESC
                """)
            return cursor.fetchall()

    def add_feedback(self, name_author, f_type, description,priority):
        """Adds a new feedback"""
        curren_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.get_connection_feedback() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback(date, name, type, description, status, resolution_note, priority) VALUES (?, ?, ?, ?, ?, ?, ?)""", (curren_data, name_author, f_type, description, "New", "", priority))
            conn.commit()

    def get_all_feedback(self):
        """Gets all feedback"""
        with self.get_connection_feedback() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id, date, name, type, description, status, resolution_note, priority FROM feedback""")
            return cursor.fetchall()








