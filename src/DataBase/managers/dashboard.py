
from DataBase.db_manager import DatabaseManager

class DashboardManager(DatabaseManager):
    def __init__(self, db_path=None):
        super().__init__(db_path)
        self.init_db()


