import sqlite3
import os
import sys
import json
from datetime import datetime
from src.DataBase.db_manager import DatabaseManager

class TransactionManager(DatabaseManager):
    """Манажер для работы с транзакциями в базе данных"""
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
            cursor.execute("""DELETE FROM transactions WHERE id = ?""", (t_id,))
            conn.commit()
            print(f"Transaction {t_id} deleted successfully")

    def get_all_transactions(self):
        """Get all transactions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id,date,type, category, sum, status 
                FROM transactions 
                ORDER BY date DESC
                """)
            return cursor.fetchall()