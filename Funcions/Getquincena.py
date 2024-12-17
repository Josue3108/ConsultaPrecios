import sqlite3
from GetFortnight import get_last_fortnight
def get_sales_last_fortnight(connection):
    """
    Obtiene producto, cantidad vendida, precio unitario, precio total sin iva, precio total iva

    Parameters:
        connection: sqlite3.Connection - Conexión activa a la base de datos.

    Returns:
        dict - Información de la última quincena creada o None si no existe ninguna.
    """
    try:
        # Obtener el mes y el año actuales

        cursor = connection.cursor()
        busqueda_quincena = get_last_fortnight(connection)
        id_quincena = busqueda_quincena["id"]

        # Obtener la última quincena creada para el mes y el año actuales
        cursor.execute('''
            SELECT Products.name, Products.price,Sales.quantity, Products.price * Sales.quantity as Precio_total,
            (Products.price * 0.13) AS precio_IVA ,((Products.price * 0.13) + Products.price) * Sales.quantity as Precio_total_IVA
            FROM Sales
            INNER JOIN Products ON Sales.product_id = Producs.id
            INNER JOIN Products ON Sales.fortnight_id = SalesperFortnight.id
            WHERE  SalesperFortnight.id= ?
            ORDER BY Products.quantity DESC
        ''', (id_quincena))

        row = cursor.fetchone()

        if row:
            return {
                "name": row[0],
                "price": row[1],
                "quantity": row[2],
                "fortnight_name": row[3],
                "total_price": row[4],
                "iva": row[5],
                "total_iva_price": row[6],
                
            }
        else:
            print(f"No hay ventas registradas ")
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener la última quincena: {e}")
        return None