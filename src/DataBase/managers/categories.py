
from DataBase.db_manager import DatabaseManager

class CategoriesDB(DatabaseManager):
    def __init__(self,db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE)
            """)
            conn.commit()

            default_categories = [
                "Proveedores",
                "Ascensores",
                "Fumigación",
                "Mantenimiento puertas de garaje",
                "Mantenimiento extintores",
                "Mantenimiento y limpieza",
                "Entidad Urbanística de Conservación",
                "Reparaciones",
                "Administración",
                "Protección de datos",
                "Otros profesionales",
                "Seguro",
                "Comisiones bancarias",
                "Correos",
                "Electricidad",
                "Agua",
                "Basura y alcantarillado",
                "Vado",
                "Igic soportado",
                "Fondo de reserva 10%",
                "Sanciones tributarias",
                "Internet porteros",
                "Coordinación actividades empresariales"
            ]

            for cat_name in default_categories:
                cursor.execute("""
                    INSERT OR IGNORE INTO categories(name) VALUES(?)
                """, (cat_name,))
                conn.commit()