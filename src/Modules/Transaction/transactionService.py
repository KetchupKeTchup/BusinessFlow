import sqlite3
from src.DataBase.managers.transaction import TransactionManager

class TransactionService:
    def __init__(self, db_path=None):
        self.db = TransactionManager(db_path)

    def load_data(self):
        transactions = self.db.get_all_transactions()
        return transactions 

    def add_transaction(self,trans_type, category, amount):
        """Додає транзакцію в базу даних"""
        self.db.add_transaction(trans_type, category, amount)
    
    def delete_transaction(self, transaction_id):
        """Видаляє транзакцію з бази даних"""
        self.db.delete_transaction(transaction_id)
    