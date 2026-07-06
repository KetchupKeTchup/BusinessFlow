import sqlite3
import os
import sys
import json
from datetime import datetime
from DataBase.db_manager import DatabaseManager

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