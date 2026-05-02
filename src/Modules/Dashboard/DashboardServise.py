from src.DataBase.db_manager import FeedbackManager, BudgetsDB


class DashboardServise:
    def __init__(self):
        # Використовуємо існуючі менеджери, щоб не писати підключення з нуля
        self.feedback_db = FeedbackManager()
        self.budget_db = BudgetsDB()

    def get_pending_tasks_count(self):
        """Рахує кількість скарг зі статусом 'Нове' або 'В процесі'"""
        with self.feedback_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM feedback 
                WHERE status IN ('Нове', 'В процесі')
            """)
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_budget_summary(self, year=2026):
        """Рахує скільки грошей залишилося (План мінус Факт)"""
        stats = self.budget_db.get_budget_stats(year)
        if not stats:
            return 0.0

        total_planned = 0.0
        total_spent = 0.0

        for row in stats:
            total_planned += float(row[1]) if row[1] else 0.0
            total_spent += float(row[2]) if row[2] else 0.0

        remaining = total_planned - total_spent
        return remaining

    def get_feedback_status_counts(self):
        """Рахує кількість скарг для кожного статусу окремо"""
        with self.feedback_db.get_connection() as conn:
            cursor = conn.cursor()
            # Групуємо результати по статусу
            cursor.execute("SELECT status, COUNT(*) FROM feedback GROUP BY status")
            return cursor.fetchall()  # Поверне щось типу: [('Нове', 2), ('Вирішено', 5)]