import sqlite3
from src.DataBase.managers.transaction import TransactionManager

import os
import shutil
from datetime import datetime

class TransactionService:
    def __init__(self, db_path=None):
        self.db = TransactionManager(db_path)

    def load_data(self):
        transactions = self.db.get_all_transactions()
        return transactions 

    # def add_transaction(self,trans_type, category, amount, comment = ""):
    #     """Додає транзакцію в базу даних"""
    #     self.db.add_transaction(trans_type, category, amount, comment)

    def add_transaction(self, trans_type, category, raw_sum_text, comment="", original_file_path=None):
        # 1. Валідація (твоя перевірка на порожнечу і числа)
        if not raw_sum_text:
            return False, "Сума не може бути порожньою!"
        
        try:
            t_sum = float(raw_sum_text.replace(",", "."))
            if t_sum <= 0:
                return False, "Сума повинна бути більшою за нуль!"
            
            # --- НОВЕ: Логіка збереження файлу ---
            final_receipt_path = None
            
            if original_file_path and os.path.exists(original_file_path):
                # Створюємо папку для фактур, якщо її ще немає
                receipts_dir = os.path.join(os.getcwd(), "data", "receipts")
                os.makedirs(receipts_dir, exist_ok=True)
                
                # Створюємо унікальне ім'я файлу на основі поточного часу
                # Наприклад: receipt_20260718_101530.pdf
                ext = os.path.splitext(original_file_path)[1] # дістаємо розширення (.pdf)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"receipt_{timestamp}{ext}"
                
                final_receipt_path = os.path.join(receipts_dir, new_filename)
                
                # Фізично копіюємо файл
                shutil.copy2(original_file_path, final_receipt_path)

            # Зберігаємо в базу новий шлях (final_receipt_path)
            self.db.add_transaction(trans_type, category, t_sum, comment, final_receipt_path)
            return True, ""
            
        except ValueError:
            return False, "Будь ласка, введіть коректне число!"

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
    