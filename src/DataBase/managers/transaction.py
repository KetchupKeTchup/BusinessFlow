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
                comment TEXT,
                receipt_path TEXT
            )
            """)
            conn.commit()
            print("Database created successfully")

    def add_transaction(self, trans_type, category, amount, comment="", receipt_path= None):
        """Add a transaction to the database"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions(date, type, category, sum, comment, receipt_path)
                VALUES(?,?,?,?,?,?)
            """, (current_date, trans_type, category, amount, comment, receipt_path))
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
                SELECT id,date,type, category, sum, comment, receipt_path
                FROM transactions 
                ORDER BY date DESC
                """)
            return cursor.fetchall()
        
    def get_transaction_by_id(self, t_id):
        """Get a transaction by its ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id,date,type, category, sum, comment, receipt_path
                FROM transactions 
                WHERE id = ?
                """, (t_id,))
            return cursor.fetchone()
    
    def edit_transaction(self, t_id, trans_type, category, amount, comment="", receipt_path=None):
        """Edit a transaction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET type = ?, category = ?, sum = ?, comment = ?, receipt_path = ?
                WHERE id = ?
            """, (trans_type, category, amount, comment, receipt_path, t_id))
            conn.commit()   
    