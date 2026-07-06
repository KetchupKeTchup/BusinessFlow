from datetime import datetime
from DataBase.db_manager import DatabaseManager

class FeedbackManager(DatabaseManager):
    def __init__(self,db_path=None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        """Create the databese for feedback if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT DEFAULT 'Нове',
                    resolution_note TEXT,
                    priority TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_feedback(self, name_author, f_type, description,priority):
        """Adds a new feedback"""
        curren_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback(date, name, type, description, status, resolution_note, priority) VALUES (?, ?, ?, ?, ?, ?, ?)""", (curren_data, name_author, f_type, description, "New", "", priority))
            conn.commit()

    def get_all_feedback(self):
        """Gets all feedback"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id, date, name, type, description, status, resolution_note, priority FROM feedback""")
            return cursor.fetchall()

    def update_status(self, feedback_id, new_status):
        """Оновлює статус звернення (скарги/пропозиції) за його ID"""
        # Використовуємо підключення до БД (переконайся, що get_connection() написано так, як в інших твоїх методах)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE feedback 
                SET status = ? 
                WHERE id = ?
            """, (new_status, feedback_id))
            conn.commit()
            print(f"Статус запису з ID {feedback_id} успішно змінено на '{new_status}'")

    def get_feedback_by_id(self, f_id):
        """Отримує всі дані одного запису для заповнення вікна редагування"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (f_id,))
            return cursor.fetchone()

    def update_feedback_full(self, f_id, name, f_type, desc, priority, status, file_path):
        """Оновлює абсолютно всі поля, включно з файлом. Якщо колонки файлу немає - створює її."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Спроба оновити всі поля
                cursor.execute("""
                    UPDATE feedback 
                    SET name = ?, type = ?, description = ?, priority = ?, status = ?, file_path = ?
                    WHERE id = ?
                """, (name, f_type, desc, priority, status, file_path, f_id))
            except Exception as e:
                # Якщо таблиця стара і в ній ще немає колонки file_path
                if "no such column: file_path" in str(e).lower():
                    cursor.execute("ALTER TABLE feedback ADD COLUMN file_path TEXT")
                    # Повторюємо запит після створення колонки
                    cursor.execute("""
                        UPDATE feedback 
                        SET name = ?, type = ?, description = ?, priority = ?, status = ?, file_path = ?
                        WHERE id = ?
                    """, (name, f_type, desc, priority, status, file_path, f_id))
                else:
                    raise e
            conn.commit()