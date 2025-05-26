import sys
import os
import sqlite3

def resource_path(relative_path):
    try:
        # Si estamos en PyInstaller, esta variable existe pero NO usarla para la base de datos
        base_path = os.path.dirname(sys.executable)  # carpeta donde está el .exe
    except Exception:
        # En desarrollo (ejecutando script .py)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATABASE_NAME = resource_path("ReportePagosBVLabs.db")

def connect_to_database():
    connection = sqlite3.connect(DATABASE_NAME)
    print(f"Conectado a la base de datos: {DATABASE_NAME}")
    return connection


def table_exists(connection, table_name):
    """Verifica si una tabla existe en la base de datos."""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (table_name,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

def count_rows(connection, table_name):
    """Cuenta las filas en una tabla dada."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def create_table_products(connection):
    """Crea la tabla Products si no existe y muestra el número de registros si existe."""
    if table_exists(connection, "Products"):
        count = count_rows(connection, "Products")
        print(f"La tabla 'Products' ya existe y contiene {count} registros.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                tax_rate REAL NOT NULL DEFAULT 0.0,
                supplier TEXT NOT NULL
            );
        ''')
        connection.commit()
        print("Tabla 'Products' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'Products': {e}")
    finally:
        cursor.close()

def create_table_salesperfortnight(connection):
    """Crea la tabla SalesperFortnight si no existe y muestra el número de registros si existe."""
    if table_exists(connection, "SalesperFortnight"):
        count = count_rows(connection, "SalesperFortnight")
        print(f"La tabla 'SalesperFortnight' ya existe y contiene {count} registros.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE SalesperFortnight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                year INTEGER NOT NULL,
                fortnight_name TEXT NOT NULL
            );
        ''')
        connection.commit()
        print("Tabla 'SalesperFortnight' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'SalesperFortnight': {e}")
    finally:
        cursor.close()

def create_table_sales(connection):
    """Crea la tabla Sales si no existe y muestra el número de registros si existe."""
    if table_exists(connection, "Sales"):
        count = count_rows(connection, "Sales")
        print(f"La tabla 'Sales' ya existe y contiene {count} registros.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE Sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                fortnight_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                sale_date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES Products (id) ON DELETE CASCADE,
                FOREIGN KEY (fortnight_id) REFERENCES SalesperFortnight (id) ON DELETE CASCADE
            );
        ''')
        connection.commit()
        print("Tabla 'Sales' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'Sales': {e}")
    finally:
        cursor.close()

# Función principal para crear todas las tablas o mostrar datos existentes
def setup_database():
    connection = connect_to_database()
    create_table_products(connection)
    create_table_salesperfortnight(connection)
    create_table_sales(connection)
    connection.close()
    print("Conexión cerrada.")

if __name__ == "__main__":
    setup_database()
