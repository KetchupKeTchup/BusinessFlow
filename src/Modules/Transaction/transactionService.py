import sqlite3
from src.DataBase.managers.transaction import TransactionManager

import os
import json
import shutil
from datetime import datetime

class TransactionService:
    def __init__(self, db_path=None):
        self.db = TransactionManager(db_path)

    def load_data(self):
        transactions = self.db.get_all_transactions()
        return transactions 

    def add_transaction(self, trans_type, category, raw_sum_text, comment="", original_file_path=None):
        # 1. Валідація (твоя перевірка на порожнечу і числа)
        if not raw_sum_text:
            return False, "Сума не може бути порожньою!"
        
        try:
            t_sum = float(raw_sum_text.replace(",", "."))
            if t_sum <= 0:
                return False, "Сума повинна бути більшою за нуль!"
            
            # --- НОВЕ: Логіка збереження файлу ---
            final_receipt_path = []
            
            if original_file_path:
                # Створюємо папку для фактур, якщо її ще немає
                receipts_dir = os.path.join(os.getcwd(), "data", "receipts")
                os.makedirs(receipts_dir, exist_ok=True)
                
                for path in original_file_path:
                    if os.path.exists(path):
                        ext = os.path.splitext(path)[1]
                        # Додаємо мікросекунди (%f), щоб імена були 100% унікальними
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        new_filename = f"receipt_{timestamp}{ext}"
                        
                        final_path = os.path.join(receipts_dir, new_filename)
                        shutil.copy2(path, final_path)
                        
                        final_receipt_path.append(final_path)
            # Перетворюємо список шляхів у формат JSON для бази даних
            # Якщо файлів не було (пустий список), записуємо None
            paths_to_save = json.dumps(final_receipt_path) if final_receipt_path else None

            # Зберігаємо в базу новий шлях (final_receipt_path)
            self.db.add_transaction(trans_type, category, t_sum, comment, paths_to_save)
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
