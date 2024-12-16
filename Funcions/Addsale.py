import sqlite3
from .GetFortnight import get_last_fortnight

def Addsale(connection, prodName, quantity):
    try:
        cursor = connection.cursor()

        # Paso 1: Obtener el product_id usando el nombre del producto (prodName)
        cursor.execute('''SELECT id FROM Products WHERE name = ?''', (prodName,))
        product_row = cursor.fetchone()

        if product_row is None:
            print(f"Producto '{prodName}' no encontrado.")
            return

        product_id = product_row[0]  # Obtengo el id (primer elemento de la fila)

        # Paso 2: Obtener la última quincena creada
        last_fortnight = get_last_fortnight(connection)
        if not last_fortnight:
            print("No se encontró una quincena válida. Por favor inicializa una quincena primero.")
            return

        fortnight_id = last_fortnight["id"]  # Asegúrate de usar el campo 'id' del diccionario

        # Paso 3: Insertar los datos en la tabla Sales
        cursor.execute('''
            INSERT INTO Sales (product_id, fortnight_id, quantity)
            VALUES (?, ?, ?)
        ''', (product_id, fortnight_id, quantity))

        connection.commit()
        print(f"Venta de {quantity} unidades del producto '{prodName}' registrada exitosamente.")

    except sqlite3.Error as e:
        print("Error al agregar la venta:", e)
        connection.rollback()
