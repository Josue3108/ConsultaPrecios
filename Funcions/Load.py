import sqlite3
import sys
import os

def resource_path(relative_path):
    try:
        # Si estamos en PyInstaller, esta variable existe pero NO usarla para la base de datos
        base_path = os.path.dirname(sys.executable)  # carpeta donde está el .exe
    except Exception:
        # En desarrollo (ejecutando script .py)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATABASE_NAME = resource_path("ReportePagosBVLabs.db")
def load_products():
    """
    Carga los productos desde la base de datos y devuelve una lista de tuplas (nombre, proveedor).
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, supplier FROM Products")
        products = [(row[0], row[1]) for row in cursor.fetchall()]
        conn.close()
        return products
    except sqlite3.Error as e:
        print(f"Error al cargar productos: {e}")
        return []
