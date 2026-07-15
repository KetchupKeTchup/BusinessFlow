import sqlite3
from src.DataBase.managers.transaction import TransactionManager

class TransactionService:
    def __init__(self, db_path=None):
        self.db = TransactionManager(db_path)

    def load_data(self):
        transactions = self.db.get_all_transactions()
        return transactions 

    def add_transaction(self,trans_type, category, amount, comment = ""):
        """Додає транзакцію в базу даних"""
        self.db.add_transaction(trans_type, category, amount, comment)

    def delete_transaction(self, transaction_id):
        """Видаляє транзакцію з бази даних"""
        self.db.delete_transaction(transaction_id)
    
    def edit_transaction(self, transaction_id, trans_type, category, amount, comment="", receipt_path=None):
        """Редагує транзакцію в базі даних"""
        self.db.edit_transaction(transaction_id, trans_type, category, amount, comment, receipt_path)

    def get_transaction_by_id(self, transaction_id):
        """Отримує транзакцію за її ID"""
        return self.db.get_transaction_by_id(transaction_id)

    # def browse_file(self):
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Вибрати фактуру", "", "All Files (*);;PDF (*.pdf);;Images (*.png *.jpg)")
    #     if file_name:
    #         self.file_path_input.setText(file_name)
    