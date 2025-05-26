import pandas as pd
import sqlite3
import os
import sys

def resource_path(relative_path):
    try:
        # Si estamos en PyInstaller, esta variable existe pero NO usarla para la base de datos
        base_path = os.path.dirname(sys.executable)  # carpeta donde está el .exe
    except Exception:
        # En desarrollo (ejecutando script .py)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def connect_to_database():
    """Conecta a la base de datos SQLite."""
    db_path = resource_path("ReportePagosBVLabs.db")
    return sqlite3.connect(db_path)

def import_products_from_excel(file_path):
    """
    Importa productos desde un archivo Excel a la base de datos.
    Actualiza los existentes por nombre o los inserta si no existen.
    """
    conn = None
    try:
        data = pd.read_excel(file_path, dtype={"name": str, "supplier": str})
        data.columns = data.columns.str.strip().str.lower()

        required_columns = {'name', 'price', 'tax_rate', 'supplier'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"El archivo debe contener las columnas: {required_columns}")

        data['price'] = data['price'].astype(str).str.replace(',', '').astype(float)
        data['tax_rate'] = data['tax_rate'].astype(str).str.replace(',', '').astype(float)
        data = data.dropna(subset=['name'])

        conn = connect_to_database()
        cursor = conn.cursor()

        for _, row in data.iterrows():
            cursor.execute("""
                UPDATE Products
                SET price = ?, tax_rate = ?, supplier = ?
                WHERE name = ?
            """, (row['price'], row['tax_rate'], row['supplier'], row['name']))

            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO Products (name, price, tax_rate, supplier)
                    VALUES (?, ?, ?, ?)
                """, (row['name'], row['price'], row['tax_rate'], row['supplier']))

        conn.commit()
        return True, "Productos importados correctamente."

    except Exception as e:
        return False, f"Error al importar productos: {e}"

    finally:
        if conn:
            conn.close()
