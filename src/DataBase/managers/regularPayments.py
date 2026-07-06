import sqlite3
import os
import sys
import json
from datetime import datetime
from DataBase.db_manager import DatabaseManager

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
