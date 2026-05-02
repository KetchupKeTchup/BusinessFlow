from src.DataBase.db_manager import FeedbackManager


class FeedbackService:
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