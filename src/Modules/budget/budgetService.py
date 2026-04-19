from src.DataBase.db_manager import BudgetsDB
class BudgetService:
    def __init__(self):
        self.db = BudgetsDB()
        self.add_budeg()

    def add_budget(self,name):
        pass