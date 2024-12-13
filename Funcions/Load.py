import sqlite3

DATABASE_NAME = "ReportePagosBVLabs.db"


def load_products():
    """
    Carga los productos desde la base de datos y devuelve una lista de nombres.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Products")
        products = [row[0] for row in cursor.fetchall()]
        conn.close()
        return products
    except sqlite3.Error as e:
        print(f"Error al cargar productos: {e}")
        return []
