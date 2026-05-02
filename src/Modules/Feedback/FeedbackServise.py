from src.DataBase.db_manager import FeedbackManager
import os
import shutil
from datetime import datetime


class FeedbackServise:
    def __init__(self):
        self.db = FeedbackManager()

    def get_all_feedbacks(self):
        """Отримує всі звернення з БД"""
        return self.db.get_all_feedback()

    def add_feedback(self, author_name, f_type, description, priority):
        """Додає нове звернення"""
        # Переконайся, що аргументи збігаються з тим, що очікує твій db_manager
        self.db.add_feedback(
            name_author=author_name,
            f_type=f_type,
            description=description,
            priority=priority
        )

    def update_status(self, record_id, new_status):
        """Оновлює статус звернення"""
        self.db.update_status(record_id, new_status)

    def delete_record(self, record_id):
        """Видаляє звернення з бази"""
        self.db.delete_feedback(record_id)

    def get_feedback_by_id(self, record_id):
        return self.db.get_feedback_by_id(record_id)

    def update_feedback_full(self, record_id, author_name, f_type, description, priority, status, file_path):
        final_path = file_path

        # Якщо файл вибрали, він існує, і це новий файл (не з нашої внутрішньої папки)
        if file_path and os.path.exists(file_path) and "data/feedback_files" not in file_path.replace("\\", "/"):
            save_dir = "data/feedback_files"
            os.makedirs(save_dir, exist_ok=True)

            original_filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{original_filename}"
            final_path = os.path.join(save_dir, safe_filename)

            shutil.copy2(file_path, final_path)  # Копіюємо у безпечне місце

        # Передаємо в БД безпечний внутрішній шлях
        self.db.update_feedback_full(record_id, author_name, f_type, description, priority, status, final_path)