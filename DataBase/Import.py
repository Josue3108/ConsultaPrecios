import pandas as pd
import sqlite3

# Nombre de la base de datos
DATABASE_NAME = "ReportePagosBVLabs.db"

def import_products_from_excel(file_path):
    """
    Importa productos desde un archivo Excel a la tabla Products en la base de datos.
    :param file_path: Ruta del archivo Excel.
    """
    try:
        # Leer el archivo Excel
        data = pd.read_excel(file_path)

        # Validar las columnas requeridas
        required_columns = {'name', 'price'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"El archivo debe contener las columnas: {required_columns}")

        # Conectar a la base de datos
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Insertar los datos en la tabla Products
        for _, row in data.iterrows():
            cursor.execute(
                "INSERT INTO Products (name, price) VALUES (?, ?)",
                (row['name'], row['price'])
            )

        conn.commit()
        conn.close()

        print("Los productos se han importado exitosamente.")
    except Exception as e:
        print(f"Error al importar productos: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    file_path = "C:/Users/yangr/Desktop/ConsultaPrecios/PRECIOS_LAB_SJ.xlsx"

    import_products_from_excel(file_path)
